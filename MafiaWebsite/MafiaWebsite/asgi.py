import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import GameRoom.routing  # Iekļaujiet savu WebSocket maršrutētāju

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MafiaWebsite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            GameRoom.routing.websocket_urlpatterns
        )
    ),
})
