# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'game_room_{self.room_code}'

        # Pievienojam lietotāju grupai
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Izdzēšam lietotāju no grupas, kad viņi atvienojas
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Atkarībā no jūsu izpildītās darbības, saglabājiet vajadzīgos dati datu bāzē un atjaunojiet cilvēku skaitu
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Atjaunojiet cilvēku skaitu un raidiet to atpakaļ visiem lietotājiem
        await self.update_player_count()

    async def update_player_count(self):
        # Pieprasiet aktualizētu cilvēku skaitu no servera
        await self.send(text_data=json.dumps({
            'type': 'player_count.update',
            'count': self.get_player_count()  # Jādefinē funkcija get_player_count, lai iegūtu cilvēku skaitu
        }))

    async def player_count_update(self, event):
        # Atjaunojiet cilvēku skaitu klienta puses WebSocket savienojumā
        count = event['count']
        await self.send(text_data=json.dumps({
            'type': 'player_count.update',
            'count': count
        }))
