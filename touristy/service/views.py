from django.shortcuts import render
from django.contrib.auth import logout
from django.http import JsonResponse

# Create your views here.

#@login_required(login_url='/account/login/')

def nearby(request):
    return render(request, 'service/nearby/nearby.html', {
        "user" : request.user.is_authenticated
    })

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