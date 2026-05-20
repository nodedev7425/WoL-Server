from wakeonlan import send_magic_packet

from django.db import transaction
from django.utils import timezone

from api.models import Device

class WakeService:

    @staticmethod
    def wake_device(mac_address):

        send_magic_packet(mac_address)

        Device.objects.filter(mac=mac_address).update(
            last_wake=timezone.now()
        )
