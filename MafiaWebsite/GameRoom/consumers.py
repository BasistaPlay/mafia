from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async, async_to_sync
from django.db import transaction
from .models import Player, GameRoom, Chat


class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"room_{self.room_code}"

        self.room = await self.get_room_data(self.room_code)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.join_room()

    async def disconnect(self, close_code):
        await self.leave_room()
        await self.update_player_list()
        await self.update_player_count()

    async def join_room(self):
        player_username = self.scope['user'].username
        message_join = f"{player_username} has joined the room."
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join_message',
                'message_join': message_join,
            }

        )
        await self.update_player_list()
        await self.update_player_count()

    @sync_to_async
    def delete_player_from_db(self, player_id, room_code):
        try:
            player = Player.objects.get(
                user_id=player_id, room__code=room_code)
            player.delete()
            print(
                f"Player with ID: {player_id} deleted successfully from room: {room_code}")
        except Player.DoesNotExist:
            print(
                f"Player with ID: {player_id} not found in room: {room_code}")

    @sync_to_async
    def find_new_owner(self, room_code):
        new_owner = Player.objects.filter(room__code=room_code).first()
        print(new_owner)
        return new_owner

    @sync_to_async
    def save_new_owner(self, new_owner):
        new_owner.save()

    async def leave_room(self):
        player_id = self.scope['user'].id
        player_username = self.scope['user'].username

        player = await self.get_player(player_id, self.room_code)

        if player:
            is_owner = player.is_owner

            await sync_to_async(transaction.set_autocommit)(False)

            await self.delete_player_from_db(player_id, self.room_code)
            await self.update_player_list()

            if is_owner:
                new_owner = await self.find_new_owner(self.room_code)
                if new_owner:
                    new_owner.is_owner = True
                    await self.save_new_owner(new_owner)

            await sync_to_async(transaction.commit)()

            message_leave = f"{player_username} has left the room."
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'leave_message',
                    'message_leave': message_leave,
                }
            )

    @sync_to_async
    def get_player(self, player_id, room_code):
        try:
            return Player.objects.get(user_id=player_id, room__code=room_code)
        except Player.DoesNotExist:
            return None

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'message' in data:
            message = data['message']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'username': data['username'],
                }
            )
        if 'startGame' in data and data['startGame']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'start_game_message',
                }
            )

    async def leave_message(self, event):
        message_leave = event['message_leave']
        await self.send(text_data=json.dumps({'message_leave': message_leave}))

    async def join_message(self, event):
        message_join = event['message_join']
        await self.send(text_data=json.dumps({'message_join': message_join}))

    async def start_game_message(self, event):
        await self.send(text_data=json.dumps({'startGame': True}))

    async def update_player_list(self):
        player_list = await self.get_player_list()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_list_update',
                'player_list': player_list,
            }
        )

    @sync_to_async
    def get_player_list(self):
        # Iegūstiet spēlētāju sarakstu no datu bāzes
        players = Player.objects.filter(room__code=self.room_code)
        player_list = []
        for player in players:
            player_data = {
                'id': player.id,
                'username': player.user.username,
                'is_owner': player.is_owner,
            }
            player_list.append(player_data)
        return player_list

    async def player_list_update(self, event):
        player_list = event['player_list']
        await self.update_player_count()
        await self.send(text_data=json.dumps({'player_list': player_list}))

    async def update_player_count(self):
        player_count = await self.get_player_count()
        max_players = self.room.max_players

        # Pārsūta informāciju par spēlētāju skaitu klientam
        await self.send(text_data=json.dumps({
            'player_count': player_count,
            'max_players': max_players,
        }))

    @sync_to_async
    def get_player_count(self):
        return Player.objects.filter(room__code=self.room_code).count()

    @sync_to_async
    def get_room_data(self, room_code):
        try:
            return GameRoom.objects.get(code=room_code)
        except GameRoom.DoesNotExist:
            return None


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"chat_{self.room_name}"

        # Pievienojam grupu
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Atvienojam no grupas
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Šeit jūs iegūstat lietotājvārdu
        username = self.scope["user"].username

        # Sūtam ziņojumu grupai
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Sūtam ziņojumu WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
