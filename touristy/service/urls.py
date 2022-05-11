from django.urls import path
from . import views

urlpatterns = [
    path('nearby/', views.nearby, name='nearby'),
    path('ajax_test/', views.ajax_test, name='ajax_test'),
    path('db_insert/', views.db_insert, name='db_insert'),
]