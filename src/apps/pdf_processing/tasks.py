import io
from io import BytesIO

from django.core.files.base import ContentFile
from pypdf import PdfReader, PdfWriter

from config.celery import app
from src.apps.notifications.tasks import send_notification
from src.apps.pdf_processing.models import File


@app.task
def extract_text_from_pdf(file_path, file_id):
    with open(file_path, 'rb') as file:
        reader = PdfReader(BytesIO(file.read()))

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    text = text.replace('\n', '\r\n')

    file_obj = File()
    file_obj.file.save(f'result_{file_id}.txt', ContentFile(text))

    send_notification.delay({'content': file_obj.file.url}, file_id)


@app.task
def pdf_encrypt(file_path, file_id, password):
    with open(file_path, 'rb') as file:
        reader = PdfReader(BytesIO(file.read()))

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.encrypt(password, algorithm="AES-256")

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    file_obj = File()
    file_obj.file.save(f'result_{file_id}.pdf', ContentFile(output.getvalue()))

    output.close()

    send_notification.delay({'content': file_obj.file.url}, file_id)


@app.task
def pdf_decrypt(file_path, file_id, password):
    with open(file_path, 'rb') as file:
        reader = PdfReader(BytesIO(file.read()))

    reader.decrypt(password)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    file_obj = File()
    file_obj.file.save(f'result_{file_id}.pdf', ContentFile(output.getvalue()))

    output.close()

    send_notification.delay({'content': file_obj.file.url}, file_id)
