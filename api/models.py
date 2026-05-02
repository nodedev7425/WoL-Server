import uuid
from datetime import datetime

from django.db import models
from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser


mac_validator = RegexValidator(
    regex=r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$',
    message='Enter a valid MAC address (e.g. AA:BB:CC:DD:EE:FF)'
)


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name =  models.CharField(max_length=255)
    mac = models.CharField(max_length=17, unique=True, validators=[mac_validator])
    last_wake = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    devices = models.ManyToManyField(Device)