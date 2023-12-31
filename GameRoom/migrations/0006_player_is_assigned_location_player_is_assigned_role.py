# Generated by Django 4.2.3 on 2023-08-02 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameRoom', '0005_player_location_player_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_assigned_location',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='is_assigned_role',
            field=models.BooleanField(default=False),
        ),
    ]
