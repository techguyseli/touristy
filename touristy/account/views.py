from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

from .forms import RegisterUserForm

# check_password(plaintext, hashed)

# Create your views here.
def login(request):
    # code here, in case successful login, redirect to service/nearby route
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        User = authenticate(request,username=username,password=password)
        if User is not None:
            login(request,User)
            return redirect("service/nearby/nearby.html")
    return render(request, "account/login/login.html")

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        # validate form
        if form.is_valid():
            form_username = form.cleaned_data['username']
            form_password = form.cleaned_data['password']
            form_password_repeat = form.cleaned_data['password_repeat']

            # validate passwords matching
            if form_password != form_password_repeat:
                return render(request, "account/register/register.html", {
                    "message" : "Password and password confirmation do not match, please try again."
                })

            # validate username existance
            if User.objects.filter(username=form_username).first() is not None:
                return render(request, "account/register/register.html", {
                    "message" : "Username already exists, please try again."
                })

            # if all good, add user and redirect to login
            user = User.objects.create_user(username=form_username, password=form_password)
            return redirect("login")

        return render(request, "account/register/register.html", {
            "message" : "The form you submitted is invalid, please try again."
        })

    return render(request, "account/register/register.html")