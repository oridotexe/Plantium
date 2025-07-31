"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
# from .views import home, plants, signup, exit, dashboard, create_crop, delete_crop, my_crops, update_crop, culminate_crop, recover_crop, deleted_crops
from .views import * 

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('plants/', plants, name='plants'),
    path('signup/', signup, name='signup'), 
    path('crop/create/', create_crop, name='create_crop'), 
    path('crop/<int:id_crop>/update/', update_crop, name='update_crop'), 
    path('crop/<int:id_crop>/delete/', delete_crop, name='delete_crop'),
    path('crop/<int:id_crop>/culminate/', culminate_crop, name='culminate_crop'),
    path('crop/deleted/<int:id_crop>/recover/', recover_crop, name='recover_crop'),
    path('crop/deleted/', deleted_crops, name='deleted_crops'),
    path('crop/', my_crops, name='my_crops'),
    path('exit/', exit, name='exit'),
]
