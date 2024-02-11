import io
import os
import re

from config.settings.base import MEDIA_ROOT

page_sizes = {
    'Portrait': {
        "A3": {"width": 297, "height": 420},
        "A4": {"width": 210, "height": 297},
        "A5": {"width": 148, "height": 210},
        "US Letter": {"width": 216, "height": 279},
        "US Legal": {"width": 216, "height": 356},
    },
    'Landscape': {
        "A3": {"width": 420, "height": 297},
        "A4": {"width": 297, "height": 210},
        "A5": {"width": 210, "height": 148},
        "US Letter": {"width": 279, "height": 216},
        "US Legal": {"width": 356, "height": 216},
    }
}


def check_password(password, max_length=30):
    if len(password) > max_length:
        return False

    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    return pattern_password.match(password)


def full_path(file_path):
    return os.path.join(MEDIA_ROOT, file_path)


def get_page_size(size, orientation):
    return page_sizes[orientation][size]
