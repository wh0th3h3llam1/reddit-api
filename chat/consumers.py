from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels_redis.core import RedisChannelLayer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    channel_layer: RedisChannelLayer

    async def connect(self):
        self.user = self.scope["user"]

        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]

        await self.channel_layer.group_

        await super().accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard()
