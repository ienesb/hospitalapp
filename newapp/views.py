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
        
        appointments = []
        for i,q in enumerate(qset):
            if not q.is_active() == "Active":
                break
            appointments.append(q)

        if len(appointments) > 5:
            appointments = appointments[:5]
        return render(request, "newhome.html", {"appointments": appointments[::-1], "length": len(qset)})


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

    def post(self, request, pk=None):
        form = NewAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.date = form.cleaned_data.get('date')
            appointment.save()
            return redirect("appointments")
        print("form is not valid")
        return redirect("newappointment")


def getdep(request, pk):
    j = json.dumps({"dep": Doctor.objects.get(pk=pk).department, "pk": pk})
    return HttpResponse(j)


@method_decorator(login_required, name='dispatch')
class EditAppointment(View):
    def get(self, request, pk):
        if not hasattr(request.user,"patient"):
            raise Http404("an error")
        
        appointment = Appointment.objects.get(pk=pk)
        doctor = appointment.doctor
        department = doctor.department
        dt = appointment.date
        session = appointment.session
        date = datetime.datetime.strftime(dt, "%m/%d/%Y")
        form = NewAppointmentForm(initial={"department": doctor.department ,"doctor": doctor, "date": date, "session": session})
        
        return render(request, "editappointment.html", {"form": form})
    
    def post(self, request, pk):
        form = NewAppointmentForm(request.POST)
        if form.is_valid():
            appointment = Appointment.objects.filter(pk=pk)
            doctor = form.cleaned_data.get('doctor')
            date = form.cleaned_data.get('date')
            session = form.cleaned_data.get('session')
            appointment.update(doctor=doctor, date=date, session=session)
            appointment[0].save()
            return redirect("appointments")
        print("form is not valid")
        return redirect(f"editappointment/{pk}")
    

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


@method_decorator(login_required, name='dispatch')
class Upload(View):
    def get(self, request, pk=0):
        if not hasattr(request.user, "doctor"):
            raise Http404("an error")
        if pk:
            patient = Patient.objects.get(pk=pk)
            form = UploadForm(initial={"patient": patient})
        else:
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


@method_decorator(login_required, name='dispatch')
class EditResult(View):
    def get(self, request, pk):
        if not hasattr(request.user, "doctor"):
            raise Http404("an error")
        result = Result.objects.get(pk=pk)
        form = UploadForm(initial={"patient": result.patient, "image": result.image})
        return render(request, "upload.html", {"form": form})
    
    def post(self, request, pk):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = Result.objects.get(pk=pk)
            doctor = result.uploaded_by
            date = result.date
            result.delete()

            result = form.save(commit=False)
            result.uploaded_by = request.user.doctor
            result.date = date
            result.save()

            return redirect("myresults")
        print("form is not valid")
        return redirect(f"editresult/{pk}")
        

@method_decorator(login_required, name='dispatch')
class DisplayResult(View):
    def get(self, request, pk):
        result = Result.objects.get(pk=pk)
        return render(request, "display.html", {"result": result})


@method_decorator(login_required, name='dispatch')
class MyAccount(View):
    def get(self, request):
        if hasattr(request.user, "patient"):
            initialValues={
            'first_name':request.user.patient.first_name,
            'last_name':request.user.patient.last_name,
            'photo': request.user.patient.photo,
            'email': request.user.email
            }
            form = MyAccountPatientForm(request.user, initial=initialValues)
        else:
            initialValues={
            'first_name':request.user.doctor.first_name,
            'last_name':request.user.doctor.last_name,
            'photo': request.user.doctor.photo,
            'email': request.doctor.email
            }
            form = MyAccountDoctorForm(request.user, initial=initialValues)
        
        return render(request, "myaccount.html", {"form": form})

    def post(self, request):
        if hasattr(request.user, "patient"):
            initialValues={
            'first_name':request.user.patient.first_name,
            'last_name':request.user.patient.first_name,
            'photo': request.user.patient.photo,
            'email': request.user.email
            }
            form = MyAccountPatientForm(request.user, request.POST, request.FILES, initial=initialValues)
            if form.is_valid():
                request.user.patient = form.save(commit=False)
                request.user.patient.save()
                request.user.email = form.cleaned_data["email"]
                request.user.save()
                return redirect("newhome")

        else:
            initialValues={
            'first_name':request.user.doctor.first_name,
            'last_name':request.user.doctor.first_name,
            'photo': request.user.doctor.photo,
            'email': request.user.email
            }
            form = MyAccountPatientForm(request.user, request.POST, request.FILES, initial=initialValues)
            if form.is_valid():
                request.user.doctor = form.save(commit=False)
                request.user.doctor.save()
                request.user.email = form.cleaned_data["email"]
                request.user.save()
                return redirect("newhome")

        print("form is not valid")
        return redirect("myaccount")


@method_decorator(login_required, name='dispatch')
class DoctorList(View):
    def get(self, request):
        doctors = Doctor.objects.all()
        return render(request, "doctorlist.html", {"doctors": doctors})


@method_decorator(login_required, name='dispatch')
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