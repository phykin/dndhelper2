# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Registration, Login

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", Registration.as_view(), name="register"),
]