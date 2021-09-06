from django import forms
from django.db.models import fields
from .models import *
import datetime

class NewAppointmentForm(forms.ModelForm):
    deps = list(Doctor.DEPARTMENTS)
    deps.insert(0,("--------","--------"))
    deps = tuple(deps)
    department = forms.ChoiceField(choices = deps, required=True)
    
    date = forms.DateField(input_formats=['%m/%d/%Y'])
    field_order = ["department", "doctor", "date", "session"]
   
    class Meta:
        model = Appointment
        fields = ["doctor", "session"]

class UploadForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["patient", "image"]

class MyAccountForm(forms.ModelForm):
    """
    picture
    first_name
    last_name
    email
    date_of_birth
    """

    def __init__(self, user, *args, **kwargs):
        super(MyAccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(initial=user.patient.first_name)
        self.fields['last_name'] = forms.CharField(initial=user.patient.last_name)
        self.fields['email'] = forms.EmailField(initial=user.email)
        self.fields['photo'] = forms.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "photo"]