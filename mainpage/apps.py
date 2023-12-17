from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate

class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainpage'
    verbose_name = 'Mainpage'

    def ready(self):
        post_migrate.connect(self.run_after_migration, sender=self)

    def run_after_migration(self, **kwargs):
        # Izpildiet delete_unverified_profiles komandu šeit
        call_command('delete_unverified_profiles')

