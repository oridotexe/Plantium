from django.urls import path
from .views import * 

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('plants/', plants, name='plants'),
    path('register/', register, name='register'),
    path('about-us/', about_us, name='about_us'),
    path('crop/create/', create_crop, name='create_crop'),
    path('crop/create/<int:plant_id>/', create_crop, name='create_crop_with_plant'), 
    path('crop/<int:id_crop>/update/', update_crop, name='update_crop'), 
    path('crop/<int:id_crop>/delete/', delete_crop, name='delete_crop'),
    path('crop/<int:id_crop>/culminate/', culminate_crop, name='culminate_crop'),
    path('crop/deleted/<int:id_crop>/recover/', recover_crop, name='recover_crop'),
    path('crop/deleted/', deleted_crops, name='deleted_crops'),
    path('crop/', my_crops, name='my_crops'),
    path('exit/', exit, name='exit'),
]
