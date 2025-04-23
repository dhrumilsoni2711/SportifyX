from django.urls import path,re_path
from .consumers import PlayerConsumer
from playerapp.consumers import ChatConsumer 

websocket_urlpatterns = [
    path("ws/players/", PlayerConsumer.as_asgi()),
    path("ws/chat/<int:receiver_id>/", ChatConsumer.as_asgi()),  # ✅ Include receiver_id in the URL
]
