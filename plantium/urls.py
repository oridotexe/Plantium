from django.urls import path
from .views import home, plants, register, exit, dashboard, create_crop, delete_crop, my_crops

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('plants/', plants, name='plants'),
    path('register/', register, name='register'), 
    path('crop/create', create_crop, name='create_crop'), 
    path('crop/<int:id_crop>/delete/', delete_crop, name='delete_crop'),
    path('crop/', my_crops, name='my_crops'),
    path('exit/', exit, name='exit'),
]
