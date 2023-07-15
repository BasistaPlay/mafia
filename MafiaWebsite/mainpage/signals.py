from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mainpage.models import Profile
from django.utils import timezone
from django.core.management import call_command

@receiver(post_save, sender=User)
def schedule_profile_deletion(sender, instance, created, **kwargs):
    if created:
        # Saglabā informāciju par e-pasta apstiprinājuma sūtīšanas laiku
        profile = Profile.objects.create(user=instance, verification_sent_at=timezone.now())
        profile.save()

        # Ieplāno profilu dzēšanu pēc norādītā laika
        call_command('delete_unverified_profiles', str(profile.id), delay=1)  # Dzēst pēc 1 stundas
