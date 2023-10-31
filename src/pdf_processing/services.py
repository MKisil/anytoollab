import io
import re

from pypdf import PdfReader, PdfWriter


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.replace('\n', '\r\n')


def check_password(password, max_length=30):
    if len(password) > max_length:
        return False

    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    return pattern_password.match(password)


def pdf_protect(pdf_file, password):
    reader = PdfReader(pdf_file)

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.encrypt(password)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return output
