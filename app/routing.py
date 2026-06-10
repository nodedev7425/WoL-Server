from django.urls import path

from api.consumers import DeviceStatusConsumer

websocket_urlpatterns = [
    path(
        'ws/devices/updates/',
        DeviceStatusConsumer.as_asgi(),
    ),
]