from django.utils import timezone

from config.celery import app
from src.apps.pdf_processing.models import File


@app.task
def delete_unnecessary_files():
    current_time = timezone.now()

    old_files = File.objects.filter(time_add__lte=current_time - timezone.timedelta(hours=1))

    old_files.delete()
