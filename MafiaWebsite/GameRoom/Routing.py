from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/some_path/(?P<room_code>\w+)/$', consumers.GameRoomConsumer.as_asgi()),
]