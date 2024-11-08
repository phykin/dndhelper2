from django.urls import path
from .views import DMControlPanelView, PlayerView, Home

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("dm/", DMControlPanelView.as_view(), name="dm_control_panel"),
    path("player/", PlayerView.as_view(), name="player_view"),
]