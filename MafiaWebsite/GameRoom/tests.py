from django.test import TestCase

# Create your tests here.
from asgiref.testing import ApplicationCommunicator
from channels.layers import get_channel_layer
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from GameRoom.consumers import RoomConsumer

User = get_user_model()

@pytest.mark.asyncio
async def test_websocket_connect():
    user = User.objects.create_user(username='testuser', password='testpassword')
    communicator = ApplicationCommunicator(RoomConsumer.as_asgi(), {'type': 'websocket.connect', 'user': user})
    connected, _ = await communicator.connect()
    assert connected is True
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_websocket_receive():
    user = User.objects.create_user(username='testuser', password='testpassword')
    communicator = ApplicationCommunicator(RoomConsumer.as_asgi(), {'type': 'websocket.connect', 'user': user})
    connected, _ = await communicator.connect()
    assert connected is True

    await communicator.send_json_to({'type': 'chat_message', 'message': 'Test message'})
    response = await communicator.receive_json_from()
    assert response['message'] == 'You said: Test message'

    await communicator.disconnect()

@pytest.mark.asyncio
async def test_websocket_disconnect():
    user = User.objects.create_user(username='testuser', password='testpassword')
    communicator = ApplicationCommunicator(RoomConsumer.as_asgi(), {'type': 'websocket.connect', 'user': user})
    connected, _ = await communicator.connect()
    assert connected is True
    await communicator.disconnect()
