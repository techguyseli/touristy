from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('edit_service/', views.edit_service, name='edit_service'),
    path('add_favourite/', views.add_favourite, name='add_favourite'),
    path('favorites_info/', views.favorites_info, name='favorites_info'),
    path('remove_favorite/<int:fav_id>', views.remove_favorite, name='remove_favorite'),
    path('add_rating/', views.add_rating, name='add_rating'),
    path('remove_rating/', views.remove_rating, name='remove_rating'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('delete_account/', views.delete_account, name='delete_account'),
]