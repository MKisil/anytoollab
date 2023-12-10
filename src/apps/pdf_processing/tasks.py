from io import BytesIO

from pypdf import PdfReader

from config.celery import app
from src.apps.notifications.tasks import send_notification


@app.task
def extract_text_from_pdf(file_path, file_id):
    with open(file_path, 'rb') as file:
        reader = PdfReader(BytesIO(file.read()))

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    text = text.replace('\n', '\r\n')

    send_notification.delay(text, file_id)
