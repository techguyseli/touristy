from django.shortcuts import render

# Create your views here.

def nearby(request):
    return render(request, 'service/nearby/nearby.html')