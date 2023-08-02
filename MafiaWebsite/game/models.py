from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    is_alive = models.BooleanField(default=True)

class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()