import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.db import transaction
from .models import Player, GameRoom
from channels.db import database_sync_to_async
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist


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
        await self.check_room_status()

    async def disconnect(self, close_code):
        await self.leave_room()
        await self.update_player_list()
        await self.update_player_count()
        await self.check_room_status()

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
        await self.send_leave_message(player_username)
        await self.check_room_status()

    async def send_leave_message(self, player_username):
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

        if 'startGame' in data:
            await self.start_game()

    async def leave_message(self, event):
        message_leave = event['message_leave']
        await self.send(text_data=json.dumps({'message_leave': message_leave}))

    async def join_message(self, event):
        message_join = event['message_join']
        await self.send(text_data=json.dumps({'message_join': message_join}))

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
        game_room = await sync_to_async(GameRoom.objects.get)(code=self.room_code)
        player_count = await self.get_player_count()
        max_players = game_room.max_players

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


class RoomListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Izsūtam sākotnējos istabu datus klientam, kad notiek savienojums
        await self.send_room_data()

    @database_sync_to_async
    def get_rooms(self):
        rooms = GameRoom.objects.all()
        return [{'code': room.code, 'player_count': room.player_count,
                 'max_players': room.max_players, 'is_private': room.is_private} for room in rooms]

    @database_sync_to_async
    def delete_empty_rooms(self):
        empty_rooms = GameRoom.objects.filter(player_count=0)
        for room in empty_rooms:
            room.delete()

    async def send_room_data(self):
        room_data = await self.get_rooms()
        await self.send(text_data=json.dumps({
            'type': 'room_update',
            'rooms': room_data,
        }))

    @csrf_protect
    async def join_room(self, room_code, password):
        try:
            room = GameRoom.objects.get(code=room_code)
            if room.is_private and room.password != password:
                # Nosūtam kļūdas ziņojumu, ja nepareiza parole privātai istabai
                await self.send_error("Invalid password.")
            elif room.player_count < room.max_players:
                # Ja ir brīvi vieti, pievienojam lietotāju istabai
                await self.channel_layer.group_add(room_code, self.channel_name)
                room.player_count += 1
                room.save()
                await self.send_success("You have joined the room.")
                await self.send_room_data()
            else:
                # Ja istabā nav brīvu vietu, nosūtam kļūdas ziņojumu
                await self.send_error("Room is full.")
        except GameRoom.DoesNotExist:
            # Nosūtam kļūdas ziņojumu, ja istaba neeksistē
            await self.send_error("Room does not exist.")

    async def send_success(self, message):
        await self.send(json.dumps({
            'type': 'success',
            'message': message,
        }))

    async def send_error(self, error):
        await self.send(json.dumps({
            'type': 'error',
            'error': error,
        }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'get_rooms':
            await self.delete_empty_rooms()  # Izdzēšam tukšas istabas pirms sūtām datus
            await self.send_room_data()
        elif message_type == 'join_room':
            room_code = text_data_json['room_code']
            password = text_data_json.get('password', '')
            csrf_token = text_data_json.get('csrf_token', '')

            await self.join_room(room_code, password, csrf_token)

    async def join_room(self, room_code, password, csrf_token):
        if self.scope['user'].is_authenticated and csrf_token == self.scope['csrf_token']:
            try:
                room = GameRoom.objects.get(code=room_code)
                # Pārbaudiet paroli un veiciet citus pārbaudes pasākumus pirms pievienošanās
                # ...
                await self.channel_layer.group_add(room_code, self.channel_name)
                room.player_count += 1
                room.save()
                await self.send_success("You have joined the room.")
                await self.send_room_data()
            except ObjectDoesNotExist:
                await self.send_error("Room does not exist.")
        else:
            await self.send_error("Authentication failed or CSRF token is invalid.")

    async def send_success(self, message):
        await self.send(json.dumps({
            'type': 'success',
            'message': message,
        }))

    async def send_error(self, error):
        await self.send(json.dumps({
            'type': 'error',
            'error': error,
        }))
