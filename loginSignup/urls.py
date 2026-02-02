"""
URL configuration for loginSignup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
import threading
import subprocess

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),  # Include app-level URLs
]

def start_flask():
    subprocess.Popen(["python", "BioBuddyBot/main.py"])

# Start Flask when Django runs
threading.Thread(target=start_flask, daemon=True).start()

def chatbot_view(request):
    return JsonResponse({"message": "Chatbot is running!"})
