from django.db import models

# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    is_alive = models.BooleanField(default=True)


class Role(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='role_images/', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
