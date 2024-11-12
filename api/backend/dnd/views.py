import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from .models import Artwork, Message
from .forms import ArtworkUploadForm


def dm_required(user):
    return user.is_superuser

@method_decorator(user_passes_test(dm_required), name="dispatch")
class DMControlPanelView(LoginRequiredMixin, View):
    template_name = "dm_control_panel.html"

    def get(self, request, *args, **kwargs):
        upload_form = ArtworkUploadForm()
        artworks = Artwork.objects.prefetch_related('available_to', 'forced_on_profiles__user')
        players = User.objects.filter(is_superuser=False)
        return render(request, self.template_name, {
            "upload_form": upload_form,
            "artworks": artworks,
            "players": players,
        })

    def post(self, request, *args, **kwargs):
        if "upload_artwork" in request.POST:
            upload_form = ArtworkUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                title = upload_form.cleaned_data["title"]
                file = upload_form.cleaned_data["file"]
                filename = file.name

                artwork_dir = '/artwork/'
                filepath = os.path.join(artwork_dir, filename)
                with open(filepath, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                artwork = Artwork.objects.create(
                    title=title,
                    filename=filename,
                )

                return redirect("dm_control_panel")
            else:
                artworks = Artwork.objects.all()
                players = User.objects.filter(is_superuser=False)
                return render(request, self.template_name, {
                    "upload_form": upload_form,
                    "artworks": artworks,
                    "players": players,
                })
        elif "action" in request.POST:
            action = request.POST.get("action")
            artwork_id = request.POST.get("artwork_id")
            artwork = Artwork.objects.get(id=artwork_id)

            if action == "make_available":
                player_ids = request.POST.getlist("players")
                players = User.objects.filter(id__in=player_ids)
                artwork.available_to.add(*players)
            elif action == "revoke_access":
                player_ids = request.POST.getlist("players")
                players = User.objects.filter(id__in=player_ids)
                artwork.available_to.remove(*players)

                for player in players:
                    profile = player.playerprofile
                    if profile.forced_artwork == artwork:
                        profile.forced_artwork = None
                        profile.save()

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"user_{player.username}",
                        {
                            "type": "remove_force_artwork",
                        }
                    )
            elif action == "force_display":
                player_ids = request.POST.getlist("players")
                players = User.objects.filter(id__in=player_ids)
                artwork.available_to.add(*players)

                for player in players:
                    profile = player.playerprofile
                    profile.forced_artwork = artwork
                    profile.save()

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"user_{player.username}",
                        {
                            "type": "force_artwork",
                            "title": artwork.title,
                            "filename": artwork.filename,
                            "artwork_id": artwork.id,
                        }
                    )
            elif action == "remove_force_display":
                player_ids = request.POST.getlist("players")
                players = User.objects.filter(id__in=player_ids)

                for player in players:
                    profile = player.playerprofile
                    if profile.forced_artwork == artwork:
                        profile.forced_artwork = None
                        profile.save()

                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"user_{player.username}",
                        {
                            "type": "remove_force_artwork",
                        }
                    )
        
        return redirect("dm_control_panel")



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["players"] = User.objects.filter(is_superuser=False)
        context["artworks"] = Artwork.objects.all()
        context["messages"] = Message.objects.all()
        return context


class PlayerView(LoginRequiredMixin, View):
    template_name = "player_view.html"

    def get(self, request, *args, **kwargs):
        player = request.user
        profile = player.playerprofile
        available_artworks = player.available_artworks.all()
        forced_artwork = profile.forced_artwork

        if forced_artwork:
            current_artwork = forced_artwork
        else:
            current_artwork = None
        
        messages = Message.objects.filter(
            models.Q(is_global=True) | models.Q(target_player=player)
        ).order_by('-timestamp')[:20]

        return render(request, self.template_name, {
            "available_artworks": available_artworks,
            "current_artwork": current_artwork,
            "messages": messages,
        })

    def post(self, request, *args, **kwargs):
        # Not needed anymore?
        # artwork_id = request.POST.get("artwork_id")
        return redirect("player_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["artworks"] = Artwork.objects.filter(target_player=user) | Artwork.objects.filter(is_global=True)
        return context


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect(reverse_lazy("dm_control_panel"))
            else:
                return redirect(reverse_lazy("player_view"))
        
        return render(request, "login_or_register.html")