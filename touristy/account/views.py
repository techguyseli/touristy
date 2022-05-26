from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from service.models import *
from .models import *
from datetime import datetime
from .forms import RegisterUserForm


# Create your views here.
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