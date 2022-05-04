from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.

def login(request):
    # code here
    return render(request, "authentication/login/login.html")

def register(request):
    # code here
    return render(request, "authentication/register/register.html")