import json

from channels.generic.websocket import AsyncWebsocketConsumer

from config.settings.base import REDIS_INSTANCE
from src.apps.notifications.services import async_check_pdf_file_exists


class PdfProcessedNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["file_id"]
        self.room_group_name = f"download_result_{self.room_name}"

        # check if the client is already connected via websocket
        if REDIS_INSTANCE.exists(self.room_name):
            await self.close()
            return

        # check if exists a file with the file_id and if not close the connection
        file_exists = await async_check_pdf_file_exists(self.room_name)
        if not file_exists:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        REDIS_INSTANCE.set(self.room_name, "connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        REDIS_INSTANCE.delete(self.room_name)

    async def notification_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
