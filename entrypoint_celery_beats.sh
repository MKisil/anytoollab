#!/bin/sh

python manage.py migrate --noinput --settings=config.settings.production

chown -R nobody:nogroup /usr/src/app/
mkdir -p /usr/src/app/media/
chmod -R u+rwX,go+rX,go-w /usr/src/app/media/

celery --workdir=/usr/src/app -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --uid=nobody --gid=nogroup