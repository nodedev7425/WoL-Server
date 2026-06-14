from enum import Enum

from django.conf import settings
from django.core.cache import cache

from api.models import Device

from utils.iptools import get_ip_from_mac, is_ip_reachable


RESOLVING_INTERFACE = getattr(settings, "RESOLVING_INTERFACE")
IP_RESOLVING_RANGE = getattr(settings, "IP_RESOLVING_RANGE")

RESOLVING_INTERVAL = int(getattr(settings, "RESOLVING_INTERVAL"))
SCANNING_INTERVAL = int(getattr(settings, "SCANNING_INTERVAL"))


class DeviceStatus(Enum):
    UNRESOLVEABLE=1
    UNREACHABLE=2
    ONLINE=3


class ResolveService:


    @staticmethod
    def resolve_mac_address(device):

        ip_address = get_ip_from_mac(
            device['mac'],
            RESOLVING_INTERFACE,
            IP_RESOLVING_RANGE
        )

        if ip_address:
            Device.objects.filter(mac=device['mac']).update(
                last_ip=ip_address
            )


    @staticmethod
    def get_device_status(device) -> DeviceStatus:

        if device.last_ip:
            if is_ip_reachable(device.last_ip, RESOLVING_INTERFACE):
                return DeviceStatus.ONLINE

            return DeviceStatus.UNREACHABLE

        return DeviceStatus.UNRESOLVEABLE
    
    
    @staticmethod
    def get_user_device_statuses(userid):

        result = []

        devices = Device.objects.filter(user=userid)

        for device in devices:

            result.append({
                "device": str(device.id),
                "status": ResolveService.get_device_status(device)
            })

        return result
        

    @staticmethod
    def get_user_device_changes(userid):

        devices = Device.objects.filter(user=userid)

        changes = []

        for device in devices:

            new_status = ResolveService.get_device_status(device)
            last_status = cache.get(device.id)

            if last_status != new_status:

                changes.append({
                    "device": str(device.id),
                    "status": new_status
                })

            cache.set(device.id, new_status, SCANNING_INTERVAL * 2)

        return changes