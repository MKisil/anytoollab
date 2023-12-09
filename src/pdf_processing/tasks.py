import time
from io import BytesIO

from asgiref.sync import async_to_sync

from celery import shared_task
from pypdf import PdfReader
from channels.layers import get_channel_layer

from config.settings.base import REDIS_INSTANCE


@shared_task
def send_notification(message, file_id):
    channel_layer = get_channel_layer()

    # waiting for the client to connect via websocket
    connection_waiting_time = 0
    while not REDIS_INSTANCE.exists(file_id):
        if connection_waiting_time == 10:
            return
        connection_waiting_time += 1
        time.sleep(1)

    room_group_name = f'download_result_{file_id}'

    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'notification_message',
            'message': message
        }
    )


@shared_task
def extract_text_from_pdf(file_path, file_id):
    with open(file_path, 'rb') as file:
        reader = PdfReader(BytesIO(file.read()))

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    text = text.replace('\n', '\r\n')

    send_notification.delay(text, file_id)
