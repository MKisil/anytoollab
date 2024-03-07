#!/bin/sh

python manage.py migrate --noinput --settings=config.settings.local

chown -R nobody:nogroup /usr/src/app/

celery --workdir=/usr/src/app -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --uid=nobody --gid=nogroup