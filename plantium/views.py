from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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