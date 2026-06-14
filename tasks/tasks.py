import os
import logging
import sys

from enum import Enum

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from api.models import Device
from utils.iptools import get_ip_from_mac, is_ip_reachable

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
)

class DeviceStatus(Enum):
    UNRESOLVEABLE=1
    UNREACHABLE=2
    ONLINE=3

RESOLVING_INTERFACE = getattr(settings, "RESOLVING_INTERFACE")
IP_RESOLVING_RANGE = getattr(settings, "IP_RESOLVING_RANGE")

RESOLVING_INTERVAL = int(getattr(settings, "RESOLVING_INTERVAL"))
SCANNING_INTERVAL = int(getattr(settings, "SCANNING_INTERVAL"))

def ip_resolve_task():

    for device in Device.objects.all().values('mac').distinct():

        ip_address = get_ip_from_mac(device['mac'], RESOLVING_INTERFACE, IP_RESOLVING_RANGE)

        if ip_address:
            Device.objects.filter(mac=device['mac']).update(
                last_ip=ip_address
            )

def is_online_broadcast():
    
    active_device_users:dict = cache.get('active_device_users')
    
    if active_device_users:

        for userid in active_device_users.keys():

            devices = Device.objects.filter(user=userid)

            for device in devices:

                last_ip = device.last_ip
                last_status = cache.get(device.id)

                if last_ip:
                    if is_ip_reachable(last_ip, RESOLVING_INTERFACE):
                        new_status=DeviceStatus.ONLINE
                    else:
                        new_status=DeviceStatus.UNREACHABLE
                else:
                    new_status=DeviceStatus.UNRESOLVEABLE

                if last_status != new_status:

                    async_to_sync(get_channel_layer().group_send)(
                        f"user_{userid}", {
                            "type": "status_changed",
                            "device": str(device.id),
                            "status": new_status.value
                        })

                cache.set(device.id, new_status, SCANNING_INTERVAL * 2) 
        

def start_tasks():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        ip_resolve_task, 
        'interval', 
        seconds=RESOLVING_INTERVAL,
        next_run_time=timezone.now(),
        max_instances=1
    )

    scheduler.add_job(
        is_online_broadcast, 
        'interval', 
        seconds=SCANNING_INTERVAL,
        max_instances=1
    )

    scheduler.start()