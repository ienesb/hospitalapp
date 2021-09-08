from django.http.response import HttpResponse, JsonResponse
from .forms import *
from . import models
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.core import serializers
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
import datetime
import os
import mimetypes
import time

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Home(View):
    def get(self, request):
        if hasattr(request.user, "doctor"):
            qset = models.Appointment.objects.filter(doctor=request.user.doctor).order_by("-date")
        else:
            qset = models.Appointment.objects.filter(patient=request.user.patient).order_by("-date")
        if len(qset) > 5:
            qset = qset[:5]
        return render(request, "newhome.html", {"appointments": qset})

@method_decorator(login_required, name='dispatch')
class Appointments(View):
    def get(self, request):
        if hasattr(request.user, "doctor"):
            qset = models.Appointment.objects.filter(doctor=request.user.doctor).order_by("-date")
        else:
            qset = models.Appointment.objects.filter(patient=request.user.patient).order_by("-date")

        paginator = Paginator(qset, 5)
        page = request.GET.get('page', 1)

        
        try:
            appointments = paginator.page(page)
        except PageNotAnInteger:
            appointments = paginator.page(1)
        except EmptyPage:
            appointments = paginator.page(paginator.num_pages)

        return render(request, "appointments.html", {"appointments": appointments})

def removeappointment(request, pk):
    if not hasattr(request.user, "patient"):
        raise Http404("an error")
    models.Appointment.objects.get(pk=pk).delete()
    return HttpResponse("success")


@method_decorator(login_required, name='dispatch')
class NewAppointment(View):
    def get(self, request, pk=None):
        if not hasattr(request.user,"patient"):
            raise Http404("an error")
        if pk:
            doctor = Doctor.objects.get(pk=pk)
            form = NewAppointmentForm(initial={"department": doctor.department ,"doctor": doctor})
        else:
            form = NewAppointmentForm()
        return render(request, "newappointment.html", {"form": form})

    def post(self, request):
        form = NewAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.date = form.cleaned_data.get('date')
            appointment.save()
            return redirect("newhome")
        print("form is not valid")
        return redirect("newappointment")

def getdep(request, pk):
    j = json.dumps({"dep": Doctor.objects.get(pk=pk).department, "pk": pk})
    return HttpResponse(j)

@method_decorator(login_required, name='dispatch') # https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/
class Records(View):
    def get(self, request):
        records = models.Record.objects.all().order_by("date")[::-1]
        return render(request, "records.html", {"records": records})

def addrating(request):
    j = json.dumps({"date": 1})
    return HttpResponse(j)

def get_record_from_pk(request, pk):
    record = get_object_or_404(models.Record, pk=pk)
    patient_name = record.patient.get_name()
    doctor_name = record.doctor.get_name()
    dep = record.doctor.department
    date = str(record.date)
    j = json.dumps({"patient_name": patient_name,
                   "doctor_name": doctor_name, "dep": dep, "date": date})
    return HttpResponse(j)

@method_decorator(login_required, name='dispatch')
class MyResults(View):
    def get(self, request):
        results = models.Result.objects.all()
        return render(request, "myresults.html", {"results": results})

def getresult(request, pk):
    print("ol iz well")
    result = Result.objects.get(pk=pk)
    url = result.image.url
    j = json.dumps({"url": url})
    return HttpResponse(j)
    

def download(request, pk):
    result = models.Result.objects.get(pk=pk)
    if hasattr(request.user, "patient"):
        if result.patient == request.user.patient:
            file_path = result.image.path
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read())
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_path)
                    return response
        else:
            raise Http404("an error")
    
    else:
        if result.uploaded_by == request.user.doctor:
            file_path = result.image.path
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read())
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_path)
                    return response
        else:
            raise Http404("an error")

class Upload(View):
    def get(self, request):
        if not hasattr(request.user, "doctor"):
            raise Http404("an error")
        form = UploadForm()
        return render(request, "upload.html", {"form": form})
    
    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = form.save(commit=False)
            result.uploaded_by = request.user.doctor
            result.date = timezone.now()
            result.save()
            return redirect("newhome")
        print("form is not valid")
        return redirect("upload")

class DisplayResult(View):
    def get(self, request, pk):
        result = Result.objects.get(pk=pk)
        return render(request, "display.html", {"result": result})

class MyAccount(View):
    def get(self, request):
        initialValues={
        'first_name':request.user.patient.first_name,
        'last_name':request.user.patient.first_name,
        'photo': request.user.patient.photo,
        'email': request.user.email
        }
        form = MyAccountForm(request.user, initial=initialValues)
        return render(request, "myaccount.html", {"form": form})

    def post(self, request):
        
        initialValues={
        'first_name':request.user.patient.first_name,
        'last_name':request.user.patient.first_name,
        'photo': request.user.patient.photo,
        'email': request.user.email
        }
        form = MyAccountForm(request.user, request.POST, request.FILES, initial=initialValues)
        if form.is_valid():
            request.user.patient = form.save(commit=False)
            request.user.patient.save()
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            return redirect("newhome")
        print("form is not valid")
        return redirect("myaccount")

class DoctorList(View):
    def get(self, request):
        doctors = Doctor.objects.all()
        return render(request, "doctorlist.html", {"doctors": doctors})


class MyPatientList(View):
    def get(self, request):
        if not hasattr(request.user, "doctor"):
            raise Http404("you are not a doctor")
        appointments = Appointment.objects.filter(doctor = request.user.doctor)
        patients = []
        for a in appointments:
            p = a.patient
            if not p in patients:
                patients.append(p)

        return render(request, "mypatientlist.html", {"patients": patients})