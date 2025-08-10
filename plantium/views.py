from pyexpat.errors import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CreateCropForm, CustomUserCreationForm
from .models import Crop, Plant
from .utils import *
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

"""
def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            user.email = user_creation_form.cleaned_data['email']
            user.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('dashboard') # P0ll1t0893
    return render(request, 'registration/register.html', data)
"""
def register(request):
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Por favor corrige los errores marcados antes de continuar.")
    else:
        user_creation_form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': user_creation_form})

def exit(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    response = request_api('7.76694000', '-72.22500000', is_current=False)
    cleaned_data = None if response is None else process_weather_data(response)
    
    data_list = create_data_list(cleaned_data)
    if data_list is not None:
        recommended = generate_recomendations(data_list.get('temps'), data_list.get('hums'))
    
    return render(request, 'dashboard.html',{'measurements':cleaned_data})

@login_required
def plants(request):
    plants = Plant.objects.all()
    return render(request, 'plants.html', {'plants': plants})

@login_required
def my_crops(request):
    crops = Crop.objects.filter(user=request.user, status__in=[0,1]).select_related('plant').order_by('-init_date')
    actives = [crop for crop in crops if crop.status == 0]
    finished = [crop for crop in crops if crop.status == 1]

    for crop in actives:
        crop.days_remaining = calculate_next_watering(crop.last_watering, crop.plant.watering_freq)

    return render(request, 'crops.html', {'actives': actives, 'finished': finished})

@login_required
def create_crop(request):
    if request.method == 'POST':
        form = CreateCropForm(request.POST, user=request.user)
        if form.is_valid():
            new_crop = form.save(commit=False)
            new_crop.user = request.user
            new_crop.save()
            return redirect('dashboard')
    else:
        form = CreateCropForm()

    return render(request, 'create_crop.html', {'form': form})

@login_required
def delete_crop(request, id_crop):
    crop = get_object_or_404(Crop, pk=id_crop, user=request.user)
    crop.status = 2
    crop.save()
    return redirect('my_crops')

@login_required
def culminate_crop(request, id_crop):
    crop = get_object_or_404(Crop, pk=id_crop, user=request.user)
    crop.status = 1
    crop.save()
    return redirect('my_crops')

@login_required
def recover_crop(request, id_crop):
    crop = get_object_or_404(Crop, pk=id_crop, user=request.user)
    crop.status = 0
    crop.save()
    return redirect('my_crops')

@login_required
def deleted_crops(request):
    crops = Crop.objects.filter(user=request.user, status__in=[2]).select_related('plant').order_by('-init_date')
    return render(request, 'recover_crop.html', {'crops': crops})

@login_required
def update_crop(request, id_crop):
    crop = get_object_or_404(Crop, pk=id_crop, user=request.user)

    if request.method == 'GET':
        form = CreateCropForm(instance=crop)
    else:
        form = CreateCropForm(request.POST, user=request.user, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('my_crops')
        
    return render(request, 'update_crop.html', {'form': form, 'crop': crop})
