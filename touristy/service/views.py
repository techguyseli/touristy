from django.shortcuts import render
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from math import fabs
from .models import Service

# Create your views here.

#@login_required(login_url='/account/login/')

def nearby(request):
    if request.method == 'POST':
        max_distnace = 0.00021350989013413368

        user_latitude = request.POST.get('latitude')
        user_longitude = request.POST.get('longitude')

        max_latitude = user_latitude + max_distnace
        min_latitude = user_latitude - max_distnace
        max_longitude = user_longitude + max_distnace
        min_longitude = user_longitude - max_distnace

        services = Service.objects.filter(latitude__gte=min_latitude, latitude__lte=max_latitude, longitude__gte=min_longitude, longitude__lte=max_longitude)
    
    return render(request, 'service/nearby/get_coordinates.html')

def ajax_test(request):
    if request.method == 'POST':
        response = {
            'latitude': request.POST.get('latitude'),
            'longitude': request.POST.get('longitude')
        }
        return JsonResponse(response)
    return render(request, "service/ajax_test/ajax_test.html", {
        "method": request.method
    })