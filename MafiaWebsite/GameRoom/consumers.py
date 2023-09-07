from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Player

class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"room_{self.room_code}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.join_room()

    async def disconnect(self, close_code):
        await self.leave_room()

    async def join_room(self):
        player_username = self.scope['user'].username
        message = f"{player_username} has joined the room."
        print(f"Join room message: {message}")  # Pievienojiet šo rindiņu

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join_message',
                'message': message,
            }
        )

    async def leave_room(self):
        player_id = self.scope['user'].id
        player_username = self.scope['user'].username

        # Delete player from the database.
        await sync_to_async(self.delete_player_from_db)(player_id, self.room_code)

        # Send a message to other players about leaving the room.
        message = f"{player_username} has left the room."
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'leave_message',
                'message': message,
            }
        )

    def delete_player_from_db(self, player_id, room_code):
        try:
            player = Player.objects.get(user_id=player_id, room__code=room_code)
            player.delete()
            print(f"Player with ID: {player_id} deleted successfully from room: {room_code}")
        except Player.DoesNotExist:
            print(f"Player with ID: {player_id} not found in room: {room_code}")
            pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    async def leave_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    async def join_message(self, event):
        # Nosūtam ziņojumu visiem klientiem, kad kāds pievienojas istabai.
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))