from django.urls import path
from . import views
from django.urls import include
from django.urls import re_path

app_name = 'game'

urlpatterns = [
    path('start-game/<str:room_code>/', views.start_game, name='start_game'),
    path('game-page/', views.game_page, name='game_page'),
]
