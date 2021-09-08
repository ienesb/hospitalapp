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
            patient = Patient(user=user)
            patient.save()
            auth_login(request, user)
            return redirect("newhome")
    else:
        form = SignUpForm()
    return render(request,"signup.html", {"form": form})
