from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from newapp.models import Patient
from django.contrib.auth import views as auth_views

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name') 
            last_name = form.cleaned_data.get('last_name')
            patient = Patient(user=user, first_name=first_name, last_name=last_name)
            patient.save()
            auth_login(request, user)
            return redirect("newhome")
    else:
        form = SignUpForm()
    return render(request,"signup.html", {"form": form})
