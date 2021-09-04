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

@method_decorator(login_required, name='dispatch')
class NewAppointment(View):
    def get(self, request, dep=0):
        if not hasattr(request.user,"patient"):
            raise Http404("an error")
        if dep == 0:
            form = NewAppointmentForm()
        else:
            department = Doctor.DEPARTMENTS[dep-1]
            form = NewAppointmentForm(initial={"department":department})
        # print(form.fields["doctor"])
        # doctors = models.Doctor.objects.all()
        # form = NewAppointmentForm()
        return render(request, "newappointment.html", {"form": form})

    def post(self, request):
        form = NewAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.date = form.cleaned_data.get('date')
            appointment.save()
            return redirect("newhome")
        return redirect("newappointment")

        # patient = request.user.patient

        # try:
        #     doctor_name = request.POST["doctor"].split(" ")[0]
        #     doctor = models.Doctor.objects.get(first_name=doctor_name)
        # except models.Doctor.DoesNotExist:
        #     return redirect("newappointment")

        # datetime_object = datetime.datetime.strptime(request.POST["datetimepicker"], '%m/%d/%Y %I:%M %p') # 08/25/2021 3:52 PM  '%b %d %Y %I:%M%p'
        # morning_start = datetime.time(hour=10, minute=0)
        # morning_end = datetime.time(hour=12, minute=0)
        # afternoon_start = datetime.time(hour=14, minute=0)
        # afternoon_end = datetime.time(hour=17, minute=0)
        
        
        # """
        # date, time, ampm = request.POST["datetimepicker"].split(" ")
        # month, day, year = date.split("/")
        # hour, minute = time.split(":")
        # if ampm == "PM":
        #     hour = int(hour) + 12
        #     if hour == 24:
        #         hour = 0
        # print(datetime_object==datetime.datetime(year=int(year), month=int(month),
        #                                               day=int(day), hour=int(hour), minute=int(minute)))
        # """
        # if datetime_object <= datetime.datetime.now():
        #     return redirect("newappointment")    
        # if datetime_object.time() < morning_start:
        #     return redirect("newappointment")    
        # if datetime_object.time() > morning_end and datetime_object.time() < afternoon_start:
        #     return redirect("newappointment")    
        # if datetime_object.time() > afternoon_end:
        #     return redirect("newappointment")    
        # if not doctor.is_available_at(datetime_object):
        #     return redirect("newappointment")    

        # a = models.Appointment(patient=patient, doctor=doctor,
        #                        date=datetime_object)
        # a.save()
        
        # return redirect("newhome")

@method_decorator(login_required, name='dispatch')#https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/
class Records(View):
    def get(self, request):
        records = models.Record.objects.all().order_by("date")[::-1]

        return render(request, "records.html", {"records": records})


def get_record_from_pk(request, pk):
    record = get_object_or_404(models.Record, pk=pk)
    '''
    record = models.Record.objects.raw(
            f"""
            SELECT
                *
            FROM
                "newapp_record"
            INNER JOIN newapp_doctor ON doctor_id = newapp_doctor.id
            INNER JOIN newapp_patient ON patient_id = newapp_patient.id
            WHERE
                "newapp_record"."id" = {pk}

            """
        )[0]
    '''
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
        r = models.Result.objects.get(pk=6)
        return render(request, "myresults.html", {"results": results, "r":r})


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

def getdep(request, pk):
    j = json.dumps({"dep": Doctor.objects.get(pk=pk).department, "pk":pk})
    return HttpResponse(j)
