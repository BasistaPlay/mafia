from django.test import TestCase
from django.contrib.auth.models import User
from mainpage.models import Profile
from django.utils import timezone
from datetime import timedelta

class ProfileDeletionTest(TestCase):
    def test_profile_deletion(self):
        # Izveidojam lietotāju un profilu ar nepārbaudītu e-pastu
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        profile = Profile.objects.create(user=user, is_email_verified=False, verification_sent_at=timezone.now() - timedelta(hours=1))

        # Pārliecinamies, ka profils ir izveidots
        self.assertEqual(Profile.objects.count(), 1)

        # Palaistam profilu dzēšanas procesu
        Profile.objects.delete_unverified_profiles()

        # Pārliecinamies, ka profils ir dzēsts
        self.assertEqual(Profile.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)