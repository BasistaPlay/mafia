from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_code>\w+)/$',
            consumers.GameRoomConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_code>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/room-list/', consumers.RoomListConsumer.as_asgi()),
]
