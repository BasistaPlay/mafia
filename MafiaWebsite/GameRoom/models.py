from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class GameRoom(models.Model):
    code = models.CharField(max_length=6, unique=True)
    player_count = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255, blank=True, null=True)
    max_players = models.PositiveIntegerField(default=7)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=6)
        super(GameRoom, self).save(*args, **kwargs)

    def __str__(self):
        return self.code

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False) 

    def __str__(self):
        return self.user.username

class Chat(models.Model):
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room: {self.room.code} | Sender: {self.sender.username} | Message: {self.message}"