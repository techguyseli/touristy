from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import RegisterUserForm

# Create your views here.
def login(request):
    # code here, in case successful login, redirect to service/nearby route
    if request.method == 'POST':
        form_username = request.POST.get('username')
        form_password =request.POST.get('password')
        user = authenticate(request, username=form_username, password=form_password)
        if user is not None:
            dj_login(request, user)
            return redirect("nearby")
        else:
            return render(request, "account/login/login.html", {
                "message" : "Wrong username or password!"
            })
    return render(request, "account/login/login.html")

def logout(request):
    dj_logout(request)
    return redirect(reverse('nearby'))

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        # validate form
        if form.is_valid():
            form_username = form.cleaned_data['username']
            form_password = form.cleaned_data['password']
            form_password_repeat = form.cleaned_data['password_repeat']

            # validate passwords matching
            if not form.passwords_match():
                return render(request, "account/register/register.html", {
                    "message" : "Password and password confirmation did not match, please try again."
                })

            # validate username existance
            user = User.objects.filter(username=form_username).first()
            if user is not None:
                return render(request, "account/register/register.html", {
                    "message" : "Username already exists, please try another one."
                })

            # if all good, add user and redirect to login
            User.objects.create_user(username=form_username, password=form_password)
            return redirect("login")

        return render(request, "account/register/register.html", {
            "message" : "The form you submitted is invalid, please try again."
        })

    return render(request, "account/register/register.html")