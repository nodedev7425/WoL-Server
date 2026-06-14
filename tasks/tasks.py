import os
import logging
import sys

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from api.models import Device

from tasks.services import ResolveService


RESOLVING_INTERVAL = int(getattr(settings, "RESOLVING_INTERVAL"))
SCANNING_INTERVAL = int(getattr(settings, "SCANNING_INTERVAL"))


logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
)


def ip_resolve_task():

    for device in Device.objects.all().values('mac').distinct():

        ResolveService.resolve_mac_address(device)
        

def is_online_broadcast():
    
    active_device_users:dict = cache.get('active_device_users')
    
    if active_device_users:

        for userid in active_device_users.keys():

            changes = ResolveService.get_user_device_changes(userid)

            for change in changes:

                async_to_sync(get_channel_layer().group_send)(
                    f"user_{userid}",
                    {
                        "type": "status_changed",
                        "device": change['device'],
                        "status": change['status'].value
                    }
                )  
        

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