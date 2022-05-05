from django.shortcuts import render

# Create your views here.

def nearby(request, message=None):
    return render(request, 'service/nearby/nearby.html', {
        "message" : message
    })