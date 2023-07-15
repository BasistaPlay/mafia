from django.core.management.base import BaseCommand
from mainpage.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Deletes unverified profiles that have not confirmed their email within a certain time period.'

    def handle(self, *args, **options):
        # Pārbauda, vai e-pasta apstiprinājums nav veikts vairāk kā 1 minūti
        cutoff_time = timezone.now() - timezone.timedelta(minutes=30)
        unverified_profiles = Profile.objects.filter(is_email_verified=False, verification_sent_at__lt=cutoff_time)

        # Dzēš neapstiprinātos profilus, kas nav aktīvi
        deleted_profiles = 0
        for profile in unverified_profiles:
            user = profile.user
            if not user.is_active:
                user.delete()
                deleted_profiles += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_profiles} unverified profiles.'))
