from django.contrib import admin
from mainpage.models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_email_verified', 'verification_sent_at']

admin.site.register(Profile, ProfileAdmin)