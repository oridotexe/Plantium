from pyexpat.errors import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CreateCropForm
from .models import Crop

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def plants(request):
    return render(request, 'plants.html')

def signup(request):
    return render(request, 'registration/signup.html')

def exit(request):
    logout(request)
    return redirect('login')

@login_required
def my_crops(request):
    crops = Crop.objects.filter(user=request.user, status__in=[0,1]).order_by('-init_date')
    
    actives = [crop for crop in crops if crop.status == 0]
    finished = [crop for crop in crops if crop.status == 1]
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
