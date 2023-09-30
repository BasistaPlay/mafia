from django.urls import path
from . import views
from django.urls import include
from django.urls import re_path


app_name = 'GameRoom'

urlpatterns = [
    path('room/<str:room_code>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('leave-room/', views.leave_room, name='leave-room'),
]
