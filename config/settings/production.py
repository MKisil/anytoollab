from .base import *

SECRET_KEY = get_env_variable('SECRET_KEY')

DEBUG = get_env_variable('DEBUG') == 'True'

# if not DEBUG:
#     STORAGES = {
#         "staticfiles": {
#             "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#         },
#         "default": {
#             "BACKEND": "storages.backends.s3.S3Storage",
#             "OPTIONS": {
#                 'access_key': get_env_variable('AWS_ACCESS_KEY_ID'),
#                 'secret_key': get_env_variable('AWS_SECRET_ACCESS_KEY'),
#                 'bucket_name': get_env_variable('AWS_STORAGE_BUCKET_NAME'),
#                 'region_name': get_env_variable('AWS_S3_REGION_NAME'),
#                 'file_overwrite': False,
#             },
#         },
#     }
