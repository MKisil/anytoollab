import json

from channels.generic.websocket import AsyncWebsocketConsumer

from config.settings.base import REDIS_INSTANCE


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["file_id"]
        self.room_group_name = f"download_result_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        REDIS_INSTANCE.set(self.room_name, "connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        REDIS_INSTANCE.delete(self.room_name)

    async def notification_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
