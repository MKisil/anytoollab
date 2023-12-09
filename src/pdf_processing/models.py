import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models


class File(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file = models.FileField(upload_to='pdf_processing/', storage=FileSystemStorage())
    time_add = models.TimeField(auto_now_add=True)