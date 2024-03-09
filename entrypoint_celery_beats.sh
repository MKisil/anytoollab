#!/bin/sh

python manage.py migrate --noinput --settings=config.settings.production

exec celery --workdir=/usr/src/app -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
