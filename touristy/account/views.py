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
def delete_image(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
    except:
        return redirect("error", message="There was an internal server error while trying to delete the image, please try again later.", title="Internal Server Error")
    
    if image.service.user != request.user:
        return redirect("error", message="There was an internal server error while trying to delete the image, please try again later.", title="Internal Server Error")

    service_id = image.service.pk
    image.delete()
    return redirect("modify_service", service_id=service_id)


@login_required(login_url='/account/login/')
def add_image(request):
    if request.method == "POST":
        form = AddImageForm(request.POST)

        if form.is_valid():
            service_id = form.cleaned_data["service_id"]
            image_url = form.cleaned_data["image_url"]

            try:
                service = Service.objects.get(pk=service_id, user=request.user)
            except:
                return redirect("error", message="The add image form you submitted wasn't valid, retry again.", title="Invalid Form")

            images = Image.objects.filter(url=image_url, service=service)
            if images:
                return redirect("error", message="The image you tried adding already exists.", title="Invalid Form", code=500)

            image = Image(service=service, url=image_url)
            image.save()

            return redirect("modify_service", service_id=service_id)

        return redirect("error", message="The add image form you submitted wasn't valid, retry again.", title="Invalid Form")
    
    return redirect("error", message="The page you requested doesn't exist.", title="Internal Server Error")


@login_required(login_url='/account/login/')
def my_services(request):
    services = Service.objects.filter(user=request.user)

    for service in services:
        images = service.images.all()

        if images:
            service.thumbnail = images[0].url

    if not services:
        return render(request, 'service/list_services/list_services.html', {
            "services" : None,
            "page_title" : "My services",
            "msg" : "There are no services.",
            "my_services" : True
        })

    return render(request, 'service/list_services/list_services.html', {
        "services" : services,
        "page_title" : "My services",
        "msg" : None,
        "my_services" : True
    })


@login_required(login_url='/account/login/')
def add_service(request):
    if request.method == 'POST':
        form = AddServiceForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            type = form.cleaned_data["type"]
            latitude = form.cleaned_data["latitude"]
            longitude = form.cleaned_data["longitude"]

            services = Service.objects.filter(latitude=latitude, longitude=longitude, title=title)
            if services:
                return render(request, "account/add_service/add_service.html", {
                    "msg" : "A service with the same title and coordinates already exists."
                })

            s = Service(user=request.user, title=title, latitude=latitude, longitude=longitude, type=type)
            s.save()
            return redirect("my_services")
        
        return render(request, "account/add_service/add_service.html", {
            "msg" : "Something went wrong with the fields you entered make sure you filled all the fields and with proper info."
        })
        
    return render(request, "account/add_service/add_service.html")


@login_required(login_url='/account/login/')
def modify_service(request, service_id=None):
    if request.method == 'POST':
        form = ModifyServiceForm(request.POST)

        if form.is_valid():
            service_id = form.cleaned_data["service_id"]
            title = form.cleaned_data["title"]
            type = form.cleaned_data["type"]
            latitude = form.cleaned_data["latitude"]
            longitude = form.cleaned_data["longitude"]

            try:
                s = Service.objects.get(user=request.user, id=service_id)
            except:
                return redirect("error", message="Something went wrong with the form you filled, please try filling it again.", code=500, title="Internal Server Error")

            s.title = title
            s.type = type
            s.latitude = latitude
            s.longitude = longitude

            s.save()
            return redirect("modify_service", service_id=s.id)

        return redirect("error", message="Something went wrong with the form you filled, please try filling it again.", code=500, title="Internal Server Error")

    if service_id:
        try:
            service = Service.objects.get(pk=service_id, user=request.user)
        except:
            return redirect("error", message="Something went wrong, please try again.", code=500, title="Internal Server Error")

        images = service.images.all()
        return render(request, "account/modify_service/modify_service.html", {
            "service" : service,
            "images" : images
        })
        
    return redirect("error", message="Something went wrong, please try again.", code=500, title="Internal Server Error")


@login_required(login_url='/account/login/')
def delete_service(request, service_id):
    try:
        service = Service.objects.get(pk=service_id, user=request.user)
    except:
        return redirect("error", message="Something went wrong, please try again.", code=500, title="Internal Server Error")
    service.delete()
    return redirect("my_services")


@login_required(login_url='/account/login/')
def delete_account(request):
    user = request.user
    dj_logout(request)
    user.delete()
    return redirect('nearby')


@login_required(login_url='/account/login/')
def account_settings(request):
    if request.method == 'POST':
        form1 = ChangeUsernameForm(request.POST)
        form2 = ChangePasswordForm(request.POST)

        # validate form
        if form1.is_valid():
            form_username = form1.cleaned_data['username']

            # validate username existance
            users = User.objects.filter(username=form_username)
            if users is not None:
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

            # check if current password is correct
            user = authenticate(request, username=request.user.username, password=form_old_password)
            if user is None:
                return render(request, "account/account_settings/account_settings.html", {
                    "message" : "Incorrect password."
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

            return redirect("login")

        return render(request, "account/account_settings/account_settings.html", {
            "message" : "The form you submitted is invalid, please try again."
        })
        
    return render(request, "account/account_settings/account_settings.html", {
        "message" : None
    })


@login_required(login_url='/account/login/')
def add_favourite(request, service_id):
    service_id = int(service_id)
    try:
        service = Service.objects.get(pk=service_id)
    except:
        return redirect("error", message="Something went wrong, please try again.", code=500, title="Internal Server Error")
    if service not in request.user.favorites.all():
        f = Favorite(user=request.user, service=service, add_date=datetime.now())
        f.save()
        return redirect('service_info', service_id=service_id)
    return redirect("error", message="This service is alredy added to your favorites.", code=500, title="Internal Server Error")


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
def remove_favorite(request, service_id):
    try:
        s = Service.objects.get(pk=service_id)
        f = Favorite.objects.get(service=s, user=request.user)
    except:
        return redirect("error", message="There was an internal server error while trying to remove this service from your favorites, please try again later.", title="Internal Server Error")
    
    f.delete()
    return redirect('service_info', service_id=service_id)


@login_required(login_url='/account/login/')
def logout(request):
    dj_logout(request)
    return redirect(reverse('nearby'))


@login_required(login_url='/account/login/')
def add_rating(request):
    if request.method == 'POST':
        form = AddRatingForm(request.POST)

        if not form.is_valid():
            return redirect("error", message="There was an internal server error, please try again later.", title="Internal Server Error")

        stars = form.cleaned_data['stars']
        service_id = form.cleaned_data['service_id']
        comment = form.cleaned_data['comment']
        
        try:
            service = Service.objects.get(pk=service_id)
        except:
            return redirect("error", message="There was an internal server error, please try again later.", title="Internal Server Error")

        existing_rating = Rating.objects.filter(user=request.user, service=service)
        if existing_rating:
            return redirect("service_info", service_id=service_id, msg="Can't rate a service multiple times.")

        r = Rating(user=request.user, service=service, stars=stars, comment_str=comment)
        r.save()
        return redirect("service_info", service_id=service_id)
    return redirect("error", message="There was an internal server error, please try again later.", title="Internal Server Error")


@login_required(login_url='/account/login/')
def remove_rating(request, rating_id):
    try:
        rating = Rating.objects.get(pk=rating_id, user=request.user)
    except:
        return redirect("error", message="There was an internal server error while trying to delete the rating, please try again later.", title="Internal Server Error", code=500)
    service_id = rating.service.id
    rating.delete()
    return redirect("service_info", service_id=service_id)


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

    return redirect("error", message="Please logout before you visit this page", title="Internal Server Error", code=500)


def register(request):
    if not request.user.is_authenticated:
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
                users = User.objects.filter(username=form_username)
                if users:
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
        
    return redirect("error", message="Please logout before you visit this page", title="Internal Server Error", code=500)