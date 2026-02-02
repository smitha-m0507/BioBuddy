from django.urls import path
from .views import (
    signup, user_login, 
    home, equipments, experiments, 
    chemicals, chatbot, user_logout,
)

app_name = "login"

urlpatterns = [
    path("", user_login, name="login"),
    path("signup/", signup, name="signup"),
    path("home/", home, name="home"),
    path("logout/", user_logout, name="logout"),
    path("equipments/", equipments, name="equipments"),
    path("experiments/", experiments, name="experiments"),
    path("chemicals/", chemicals, name="chemicals"),
    path("chatbot/", chatbot, name="chatbot"),
]