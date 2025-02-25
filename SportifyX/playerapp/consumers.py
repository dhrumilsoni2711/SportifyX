import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Player
from geopy.distance import geodesic

class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_lat = float(data["latitude"])
        user_lon = float(data["longitude"])

        # Find nearby players
        players = Player.objects.all()
        nearby_players = []

        for player in players:
            player_location = (player.latitude, player.longitude)
            user_location = (user_lat, user_lon)

            distance = geodesic(user_location, player_location).km

            if distance <= 10:  # Players within 10 km
                nearby_players.append({
                    "username": player.user.username,
                    "sport": player.sport,
                    "distance": round(distance, 2),
                })

        await self.send(text_data=json.dumps({"players": nearby_players}))
