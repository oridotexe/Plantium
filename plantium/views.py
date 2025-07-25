from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CreateCropForm

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
def create_crop(request):
    if request.method == 'POST':
        form = CreateCropForm(request.POST)
        if form.is_valid():
            new_crop = form.save(commit=False)
            new_crop.user = request.user
            new_crop.save()
            new_crop.save()
            return redirect('dashboard')  # Cambia por tu ruta de éxito
    else:
        form = CreateCropForm()

    return render(request, 'create_crop.html', {'form': form})