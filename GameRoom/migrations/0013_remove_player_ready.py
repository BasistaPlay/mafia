# Generated by Django 4.2.3 on 2023-09-14 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GameRoom', '0012_gameroom_ready_count_player_ready'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='ready',
        ),
    ]
