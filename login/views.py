from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("login:login")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "login/signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("login:home")
        messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "login/login.html", {"form": form})

# Keep other views the same
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login:login")

@login_required
def home(request):
    return render(request, "login/home.html")

@login_required
def equipments(request):
    return render(request, "login/equipments.html")

@login_required
def experiments(request):
    return render(request, "login/experiments.html")

@login_required
def chemicals(request):
    return render(request, "login/chemicals.html")

@login_required
def chatbot(request):
    return render(request, "login/chatbot.html")
