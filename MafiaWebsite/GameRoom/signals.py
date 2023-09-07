# Jūsu projektā definējiet signālu, kas aktīvi, kad lietotājs atvienojas no istabas
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Player

@receiver(post_delete, sender=Player)
def player_disconnect(sender, instance, **kwargs):
    # Šis kods tiek izsaukts, kad kāds atvienojas no istabas (Player tiek dzēsts)
    if instance.is_owner:
        # Ja atvienojas īpašnieks, jums vajadzētu pārnest īpašnieka tiesības uz citu cilvēku
        room = instance.room
        other_players = Player.objects.filter(room=room).exclude(id=instance.id)
        if other_players.exists():
            new_owner = other_players.first()
            room.owner = new_owner.user
            room.save()
