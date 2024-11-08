from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistrationForm


class Login(LoginView):
    template_name = "login_or_register.html"

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("dm_control_panel")
        else:
            return reverse_lazy("player_view")


class Registration(CreateView):
    form_class = RegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy('login')
