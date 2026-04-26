from django.db import models

from django.contrib.auth.models import AbstractUser


class Device(models.Model):
    name =  models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    devices = models.ManyToManyField(Device)