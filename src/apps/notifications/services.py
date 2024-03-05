from channels.db import database_sync_to_async


@database_sync_to_async
def async_check_pdf_file_exists(file_id):
    from src.apps.pdf_processing.models import File
    return File.objects.filter(id=file_id).exists()
