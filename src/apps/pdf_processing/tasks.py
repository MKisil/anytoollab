import io
import zipfile

import fitz
from io import BytesIO
from unidecode import unidecode

from django.core.files.base import ContentFile
from pypdf import PdfReader, PdfWriter

from config.celery import app
from src.apps.notifications.tasks import send_notification
from src.apps.pdf_processing.models import File


@app.task
def extract_text_from_pdf(file_path, file_id):
    doc = fitz.open(file_path)

    output = []

    for page in doc:
        output += page.get_text("blocks")

    result_text = ''
    previous_block_id = 0
    for block in output:

        if block[6] == 0:

            if previous_block_id != block[5]:
                result_text += "\n"

            plain_text = unidecode(block[4])

            result_text += plain_text

    file_obj = File()
    file_obj.file.save(f'result_{file_id}.txt', ContentFile(result_text))

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


@app.task
def pdf_compress(file_path, file_id):
    with open(file_path, 'rb') as file:
        reader = PdfReader(BytesIO(file.read()))

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)

    if reader.metadata:
        writer.add_metadata(reader.metadata)

    for page in writer.pages:
        for img in page.images:
            img.replace(img.image)

    for page in writer.pages:
        page.compress_content_streams()

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    file_obj = File()
    file_obj.file.save(f'result_{file_id}.pdf', ContentFile(output.getvalue()))

    output.close()

    send_notification.delay({'content': file_obj.file.url}, file_id)


@app.task
def pdf_split(file_path, file_id, selected_pages, save_separate=False, password=''):
    selected_pages = map(lambda x: int(x), sorted(selected_pages.split(',')))

    doc = fitz.open(file_path)
    doc.authenticate(password)

    if save_separate:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip:
            for p in selected_pages:
                pdf_page = fitz.open()
                pdf_page.insert_pdf(doc, from_page=p, to_page=p)

                output = io.BytesIO()
                pdf_page.save(output)
                output.seek(0)

                zip.writestr(f'page_{p}.pdf', output.getvalue())

                pdf_page.close()
                output.close()

        zip_buffer.seek(0)

        file_obj = File()
        file_obj.file.save(f'result_{file_id}.zip', ContentFile(zip_buffer.getvalue()))

        zip_buffer.close()

        send_notification.delay({'content': file_obj.file.url}, file_id)

    else:
        new_doc = fitz.open()

        for p in selected_pages:
            new_doc.insert_pdf(doc, from_page=p, to_page=p)

        output = io.BytesIO()
        new_doc.save(output)
        output.seek(0)

        file_obj = File()
        file_obj.file.save(f'result_{file_id}.pdf', ContentFile(output.getvalue()))

        new_doc.close()
        output.close()

        send_notification.delay({'content': file_obj.file.url}, file_id)
