from django.apps import AppConfig


class GameroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GameRoom'

    def ready(self):
        import GameRoom.signals