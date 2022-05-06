from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.

def nearby(request):
    user = request.user.is_authenticated
    logout(request)
    return render(request, 'service/nearby/nearby.html', {
        "user" : user
    })