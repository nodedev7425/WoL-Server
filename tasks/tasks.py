import logging
import sys

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from api.models import Device
import os
from utils.iptools import get_ip_from_mac

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
)

RESOLVING_INTERFACE = getattr(settings, "RESOLVING_INTERFACE")
IP_RESOLVING_RANGE = getattr(settings, "IP_RESOLVING_RANGE")
RESOLVING_INTERVAL = int(getattr(settings, "RESOLVING_INTERVAL"))

def ip_resolve_task():

    for device in Device.objects.all().values('mac').distinct():

        ip_address = get_ip_from_mac(device['mac'], RESOLVING_INTERFACE, IP_RESOLVING_RANGE)

        if ip_address:
            Device.objects.filter(mac=device['mac']).update(
                last_ip=ip_address
            )

def is_online_broadcast():
    
    active_device_users:dict = cache.get('active_device_users')
    
    for key in active_device_users.keys():
        
    

def start_tasks():

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        ip_resolve_task, 
        'interval', 
        minutes=RESOLVING_INTERVAL,
        next_run_time=timezone.now(),
        max_instances=1
    )

    scheduler.add_job(
        is_online_broadcast, 
        'interval', 
        minutes=1,
        max_instances=1
    )

    scheduler.start()