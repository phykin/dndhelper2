from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class Registration(TemplateView):
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})
    
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {"form": form})
