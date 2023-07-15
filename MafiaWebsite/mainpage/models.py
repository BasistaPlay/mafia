from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProfileManager(models.Manager):
    def delete_unverified_profiles(self):
        cutoff_time = timezone.now() - timezone.timedelta(hours=1)
        unverified_profiles = self.get_queryset().filter(is_email_verified=False, verification_sent_at__lt=cutoff_time)

        for profile in unverified_profiles:
            user = profile.user
            user.delete()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    verification_sent_at = models.DateTimeField(blank=True, null=True)

    objects = ProfileManager()
