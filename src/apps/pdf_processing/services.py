import io
import os
import re

from pypdf import PdfReader, PdfWriter

from config.settings.base import MEDIA_ROOT


def check_password(password, max_length=30):
    if len(password) > max_length:
        return False

    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    return pattern_password.match(password)


def full_path(file_path):
    return os.path.join(MEDIA_ROOT, file_path)
