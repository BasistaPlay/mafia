# Generated by Django 4.2.3 on 2023-12-11 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='role_images/'),
        ),
    ]
