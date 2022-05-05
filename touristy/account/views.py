from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import RegisterForm

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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'account/register/register.html', {'form': form})