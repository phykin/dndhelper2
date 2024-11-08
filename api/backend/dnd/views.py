from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from .models import Artwork, Message


def dm_required(user):
    return user.is_superuser

@method_decorator(user_passes_test(dm_required), name="dispatch")
class DMControlPanelView(LoginRequiredMixin, TemplateView):
    template_name = "dm_control_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["players"] = User.objects.filter(is_superuser=False)
        context["artworks"] = Artwork.objects.all()
        context["messages"] = Message.objects.all()
        return context


class PlayerView(LoginRequiredMixin, TemplateView):
    template_name = "player_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["artworks"] = Artwork.objects.filter(target_player=user) | Artwork.objects.filter(is_global=True)
        context["messages"] = Message.objects.filter(target_player=user) | Message.objects.filter(is_global=True)
        return context


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect(reverse_lazy("dm_control_panel"))
            else:
                return redirect(reverse_lazy("player_view"))
        
        return render(request, "login_or_register.html")