from django.conf import settings
from django.core.cache import cache

from channels.generic.websocket import AsyncWebsocketConsumer

class DeviceStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.group_name = None         

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        # Cache user ids that are currently active

        active = await cache.aget("active_device_users", {})

        user_id = str(user.id)
        active[user_id] = active.get(user_id, 0) + 1

        await cache.aset("active_device_users", active)

        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def disconnect(self, code):
        
        if self.group_name:

            user = self.scope["user"]

            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

            # Remove active user from cache

            active = await cache.aget("active_device_users", {})

            user_id = str(user.id)

            if user_id in active:
                active[user_id] -= 1

                if active[user_id] <= 0:
                    del active[user_id]

            await cache.aset("active_device_users", active)
