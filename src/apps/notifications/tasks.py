import time

from asgiref.sync import async_to_sync

from celery import shared_task
from channels.layers import get_channel_layer

from config.settings.base import REDIS_INSTANCE


@shared_task
def send_notification(message, room_name):
    channel_layer = get_channel_layer()

    # waiting for the client to connect via websocket
    connection_waiting_time = 0
    while not REDIS_INSTANCE.exists(room_name):
        if connection_waiting_time == 15:
            return
        connection_waiting_time += 1
        time.sleep(1)

    room_group_name = f'download_result_{room_name}'

    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'notification_message',
            'message': message
        }
    )