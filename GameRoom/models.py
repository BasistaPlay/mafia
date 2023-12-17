from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save, post_delete
from game.models import Location, Role
from django.dispatch import receiver


class GameRoom(models.Model):
    code = models.CharField(max_length=6, unique=True)
    player_count = models.PositiveIntegerField(default=0)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255, blank=True, null=True)
    max_players = models.PositiveIntegerField(default=7)
    is_game_started = models.BooleanField(default=False)
    ready_count = models.PositiveIntegerField(default=0)

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
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='players_in_game')
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Player)
def update_player_count_on_player_save(sender, instance, **kwargs):
    """
    Pēc spēlētāja saglabāšanas atjauno player_count GameRoom modelī.
    """
    room = instance.room
    room.player_count = Player.objects.filter(room=room).count()
    # room.ready_count = Player.object.filter(room=room, is_ready=True).count()
    room.save()


@receiver(post_delete, sender=Player)
def update_player_count_on_player_delete(sender, instance, **kwargs):
    """
    Pēc spēlētāja dzēšanas atjauno player_count GameRoom modelī.
    """
    room = instance.room
    room.player_count = Player.objects.filter(room=room).count()
    # room.ready_count = Player.object.filter(room=room, is_ready=True).count()
    room.save()


@receiver(post_save, sender=Player)
def update_ready_count_on_player_change(sender, instance, **kwargs):
    """
    Atjauno ready_count GameRoom modelī, kad veiktas izmaiņas Player modelī.
    """
    room = instance.room
    room.player_count = Player.objects.filter(room=room).count()
    room.ready_count = Player.objects.filter(room=room, is_ready=True).count()
    room.save()
