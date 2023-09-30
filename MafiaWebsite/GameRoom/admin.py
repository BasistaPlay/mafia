from django.contrib import admin
from .models import GameRoom, Player

# Register your models here.


class GameRoomAdmin(admin.ModelAdmin):
    list_display = ('code', 'player_count', 'is_private')
    list_filter = ('is_private',)
    search_fields = ('code',)


admin.site.register(GameRoom, GameRoomAdmin)

admin.site.register(Player)
