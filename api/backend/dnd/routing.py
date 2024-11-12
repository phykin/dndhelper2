from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/dm/", consumers.DMConsumer.as_asgi()),
    path("ws/player/", consumers.PlayerConsumer.as_asgi()),
    path("ws/initiative/", consumers.InitiativeConsumer.as_asgi()),
]