from django.urls import re_path

from api.consumers import DeviceStatusConsumer

websocket_urlpatterns = [
    re_path(
        r'ws/devices/updates/',
        DeviceStatusConsumer.as_asgi(),
    ),
]