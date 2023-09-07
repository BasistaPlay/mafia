from django.urls import path
from . import views
from django.urls import include
from django.urls import re_path


app_name = 'GameRoom'

urlpatterns = [
    path('room/<str:room_code>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('send-message/<str:room_code>/', views.send_message, name='send_message'),
    path('fetch-messages/<str:room_code>/', views.fetch_messages, name='fetch_messages'),
    path('check-and-delete-room/<str:room_code>/', views.check_and_delete_room, name='check_and_delete_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('change-owner/<str:room_code>/<int:player_id>/', views.change_owner, name='change_owner'),
    path('fetch-players/<str:room_code>/', views.fetch_players, name='fetch_players'),
    path('api/get_rooms/', views.get_rooms_api, name='get_rooms_api'),
    path('check-user-status/', views.check_user_status, name='check_user_status'),
    path('get_room_data/', views.get_room_data, name='get_room_data'),
    path('leave-room/', views.leave_room, name='leave-room'),
    path('remove-player/<int:player_id>/', views.remove_player, name='remove-player'),
    path('update-player-count/<str:room_code>/', views.update_player_count, name='update_player_count'),
    path('get-player-count/<str:room_code>/', views.get_player_count, name='get-player-count'),


]
