#!/bin/sh

python manage.py migrate --noinput --settings=config.settings.local

celery --workdir=/usr/src/app -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler