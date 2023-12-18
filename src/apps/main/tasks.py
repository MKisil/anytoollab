from django.utils import timezone

from config.celery import app
from src.apps.pdf_processing.models import File


@app.task
def delete_unnecessary_files():
    # On production
    # s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
    #
    # keys_to_delete = list(old_files.values_list('file_field', flat=True))
    #
    # s3.delete_objects(
    #     Bucket='',
    #     Delete={
    #         'Objects': [{'Key': key} for key in keys_to_delete],
    #         'Quiet': False
    #     }
    # )
    current_time = timezone.now()

    old_files = File.objects.filter(time_add__lte=current_time - timezone.timedelta(hours=1))

    old_files.delete()
