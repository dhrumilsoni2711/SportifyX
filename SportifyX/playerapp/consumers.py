import json
from channels.generic.websocket import AsyncWebsocketConsumer
from geopy.distance import geodesic
from asgiref.sync import sync_to_async
from playerapp.models import User  # Use User instead of Player

from django.contrib.auth.models import User
from adminapp.models import ChatMessage
from django.utils.timezone import now

class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_lat = float(data.get("latitude", 0))
        user_lon = float(data.get("longitude", 0))

        # Get nearby players asynchronously
        nearby_players = await self.get_nearby_players(user_lat, user_lon)

        # Send response back to WebSocket
        await self.send(text_data=json.dumps({"players": nearby_players}))

    @sync_to_async
    def get_nearby_players(self, user_lat, user_lon):
        # Fetch only users with role='player' and valid GPS coordinates
        players = User.objects.filter(role='player', latitude__isnull=False, longitude__isnull=False)
        nearby_players = []

        for player in players:
            player_location = (player.latitude, player.longitude)
            user_location = (user_lat, user_lon)

            distance = geodesic(user_location, player_location).km

            if distance <= 10:  # Players within 10 km
                nearby_players.append({
                    "username": player.username,  # No need to check player.user
                    "sport": player.sport,
                    "distance": round(distance, 2),
                })

        return nearby_players

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from adminapp.models import ChatMessage
from asgiref.sync import sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        self.room_group_name = f"chat_{min(self.scope['user'].id, self.receiver_id)}_{max(self.scope['user'].id, self.receiver_id)}"

        # ✅ Add user to the WebSocket group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_id = data["sender"]
        receiver_id = data["receiver"]

        sender = await sync_to_async(User.objects.get)(id=sender_id)
        receiver = await sync_to_async(User.objects.get)(id=receiver_id)

        # ✅ Save message to the database
        await sync_to_async(ChatMessage.objects.create)(sender=sender, receiver=receiver, message=message)

        # ✅ Send message to receiver in real-time
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))
