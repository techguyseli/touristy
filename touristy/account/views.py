from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.

def login(request):
    # code here, in case successful login, redirect to service/nearby route
    return render(request, "account/login/login.html")

def register(request):
    # code here, in case successful registry, redirect to login
    return render(request, "account/register/register.html")