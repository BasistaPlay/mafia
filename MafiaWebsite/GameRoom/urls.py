from django.urls import path
from . import views
from django.urls import include
from django.urls import re_path


app_name = 'GameRoom'

urlpatterns = [
    path('room/<str:room_code>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('check-and-delete-room/<str:room_code>/',
         views.check_and_delete_room, name='check_and_delete_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('change-owner/<str:room_code>/<int:player_id>/',
         views.change_owner, name='change_owner'),
    path('api/get_rooms/', views.get_rooms_api, name='get_rooms_api'),
    path('check-user-status/', views.check_user_status, name='check_user_status'),
    path('get_room_data/', views.get_room_data, name='get_room_data'),
    path('leave-room/', views.leave_room, name='leave-room'),
    path('remove-player/<int:player_id>/',
         views.remove_player, name='remove-player'),



]
