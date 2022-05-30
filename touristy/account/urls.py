from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('add_favourite/<int:service_id>', views.add_favourite, name='add_favourite'),
    path('favorites_info/', views.favorites_info, name='favorites_info'),
    path('remove_favorite/<int:service_id>', views.remove_favorite, name='remove_favorite'),
    path('add_rating/', views.add_rating, name='add_rating'),
    path('remove_rating/', views.remove_rating, name='remove_rating'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('my_services/', views.my_services, name='my_services'),
    path('add_service/', views.add_service, name='add_service'),
    path('modify_service/', views.modify_service, name='modify_service'),
    path('modify_service/<int:service_id>', views.modify_service, name='modify_service'),
    path('delete_service/<int:service_id>', views.delete_service, name='delete_service'),
    path('add_image/', views.add_image, name='add_image'),
    path('delete_image/<int:image_id>', views.delete_image, name='delete_image'),
]