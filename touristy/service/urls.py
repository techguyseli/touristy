from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:service_id>', views.service_info, name='service_info'),
    path('<int:service_id>/<str:msg>', views.service_info, name='service_info'),
    path('nearby/', views.nearby, name='nearby'),
    path('map/', views.map, name='map'),
    path('db_insert/', views.db_insert, name='db_insert'),
    path('error/<int:code>/<str:title>/<str:message>', views.error, name='error'),
]