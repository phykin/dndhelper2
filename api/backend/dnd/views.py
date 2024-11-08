from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
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


class Home(TemplateView):
    template_name = "home.html"