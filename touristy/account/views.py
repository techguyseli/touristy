from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
def login(request):
    # code here, in case successful login, redirect to service/nearby route
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_password =request.POST.get('user_password')
        User = authenticate(request,user_id=user_id,user_password=user_password)
        if User is not None:
            login(request,User)
            return redirect("service/nearby/nearby.html")
    return render(request, "account/login/login.html")

def register(request):
    # code here, in case successful registry, redirect to login
    return render(request, "account/register/register.html")