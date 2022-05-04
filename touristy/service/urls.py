from django.urls import path
from . import views

urlpatterns = [
    path('nearby/', views.nearby, name='nearby'),
]