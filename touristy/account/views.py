from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from service.models import *
from .models import *
from datetime import datetime
from .forms import *
from django.contrib.auth.hashers import PBKDF2PasswordHasher


@login_required(login_url='/account/login/')
def delete_account(request):
    user = request.user
    dj_logout(request)
    user.delete()
    return redirect(reverse('nearby'))


@login_required(login_url='/account/login/')
def account_settings(request):
    if request.method == 'POST':
        form1 = ChangeUsernameForm(request.POST)
        form2 = ChangePasswordForm(request.POST)

        # validate form
        if form1.is_valid():
            form_username = form1.cleaned_data['username']

            # validate username existance
            user = User.objects.filter(username=form_username).first()
            if user is not None:
                return render(request, "account/account_settings/account_settings.html", {
                    "message" : "Username already exists, please try another one."
                })

            request.user.username = form_username
            request.user.save(update_fields=['username'])
            return render(request, "account/account_settings/account_settings.html", {
                "message" : None
            })

        if form2.is_valid():
            form_old_password = form2.cleaned_data['old_password']
            form_new_password = form2.cleaned_data['new_password']
            form_password_repeat = form2.cleaned_data['password_repeat']

            user = authenticate(request, username=request.user.username, password=form_old_password)
            if user is None:
                return render(request, "account/account_settings/account_settings.html", {
                    "message" : "Invalid current password."
                })

            # check if password changed
            if not form2.password_changed():
                return render(request, "account/account_settings/account_settings.html", {
                    "message" : "Password didn't change, please try again."
                })
            
            # validate new password and confirmation matching
            if not form2.new_passwords_match():
                return render(request, "account/account_settings/account_settings.html", {
                    "message" : "New password and its confirmation did not match, please try again."
                })

            hasher = PBKDF2PasswordHasher()
            algorithm, salt, hashh = request.user.password.split('$', 2)
            request.user.password = hasher.encode(form_new_password, salt)
            request.user.save(update_fields=['password'])

            return render(request, "account/account_settings/account_settings.html", {
                "message" : None
            })

        return render(request, "account/account_settings/account_settings.html", {
            "message" : "The form you submitted is invalid, please try again."
        })
        
    return render(request, "account/account_settings/account_settings.html", {
        "message" : None
    })


@login_required(login_url='/account/login/')
def add_favourite(request):
    if request.method == "POST":
        service_id = int(request.POST.get("service_id"))
        service = Service.objects.get(pk=service_id)
        if service not in request.user.favorites.all():
            f = Favorite(user=request.user, service=service, add_date=datetime.now())
            f.save()
        return redirect('service_info', service_id=service_id)
    return redirect('favorites_info')


@login_required(login_url='/account/login/')
def favorites_info(request):
    favorites = Favorite.objects.filter(user=request.user)
    for fav in favorites:
        images = fav.service.images.all()
        if images:
            fav.service.thumbnail = images[0].url
    return render(request, 'account/favorites/favorites_info.html', {
        "favorites" : favorites
    })


@login_required(login_url='/account/login/')
def edit_service(request):
    return HttpResponse('hvjbkjnl,')


@login_required(login_url='/account/login/')
def remove_favorite(request, fav_id):
    f = Favorite.objects.filter(pk=int(fav_id), user=request.user).first()
    if f:
        f.delete()
    return redirect('favorites_info')


def login(request):
    if not request.user.is_authenticated:
        # code here, in case successful login, redirect to service/nearby route
        if request.method == 'POST':
            form_username = request.POST.get('username')
            form_password = request.POST.get('password')
            user = authenticate(request, username=form_username, password=form_password)
            if user is not None:
                dj_login(request, user)
                return redirect("nearby")
            else:
                return render(request, "account/login/login.html", {
                    "message" : "Wrong username or password!"
                })
        return render(request, "account/login/login.html")


@login_required(login_url='/account/login/')
def logout(request):
    dj_logout(request)
    return redirect(reverse('nearby'))


@login_required(login_url='/account/login/')
def add_rating(request):
    if request.method == 'POST':
        stars = int(request.POST.get('stars'))

        if stars < 0 or stars > 5:
            return redirect("service_info", service_id=service_id)

        service_id = int(request.POST.get('service_id'))
        service = Service.objects.get(pk=service_id)
        comment = request.POST.get('comment')

        existing_rating = Rating.objects.filter(user=request.user, service=service)
        if existing_rating:
            return redirect("service_info", service_id=service_id, msg="Can't rate a service multiple times.")

        r = Rating(user=request.user, service=service, stars=stars, comment_str=comment)
        r.save()

    return redirect("service_info", service_id=service_id)
    

@login_required(login_url='/account/login/')
def remove_rating(request):
    service_id = int(request.POST.get('service_id'))

    if request.method == 'POST':
        rating_id = int(request.POST.get('rating_id'))
        r = Rating.objects.get(pk=rating_id, user=request.user)
        r.delete()

    return redirect("service_info", service_id=service_id)


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