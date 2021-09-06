from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime
# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=50, default="PatientName")
    last_name = models.CharField(max_length=50, default="PatientLastName")
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(upload_to="pictures", null=True)
    date_of_birth = models.DateField(null=True)
    
    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Doctor(models.Model):
    DEPARTMENTS = (
        (1,'Cardiologist'),
        (2,'Dermatologists'),
        (3,'Emergency Medicine Specialists'),
        (4,'Allergists/Immunologists'),
        (5,'Anesthesiologists'),
        (6,'Colon and Rectal Surgeons'),
        
    )
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_available_at(self, time):
        appointments = Appointment.objects.filter(doctor=self)
        for a in appointments:
            if a.date == time:
                return False

        return True
        

class Appointment(models.Model):
    SESSIONS = (
        (datetime.time(hour=10, minute=00), "10.00-10.30"),
        (datetime.time(hour=10, minute=30), "10.30-11.00"),
        (datetime.time(hour=11, minute=00), "11.00-11.30"),
        (datetime.time(hour=11, minute=30), "11.30-12.00"),
        (datetime.time(hour=14, minute=00), "14.00-14.30"),
        (datetime.time(hour=14, minute=30), "14.30-15.00"),
        (datetime.time(hour=15, minute=00), "15.00-15.30"),
        (datetime.time(hour=15, minute=30), "15.30-16.00"),
        (datetime.time(hour=16, minute=00), "16.00-16.30"),
        (datetime.time(hour=16, minute=30), "16.30-17.00"),
        
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(null=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    session = models.TimeField(choices=SESSIONS, null=True)

    def is_active(self):
        
        if self.date > timezone.now().date():
            return "Active"
        elif self.date == timezone.now().date():
            if self.session > timezone.now().time():
                return "Active"
        return "Not Active"

class Record(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class Result(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    image = models.FileField(upload_to='results')
    uploaded_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)