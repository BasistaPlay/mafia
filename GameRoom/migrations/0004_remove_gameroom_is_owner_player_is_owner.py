# Generated by Django 4.2.3 on 2023-07-22 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameRoom', '0003_gameroom_is_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameroom',
            name='is_owner',
        ),
        migrations.AddField(
            model_name='player',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
    ]
