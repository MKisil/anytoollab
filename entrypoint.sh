#!/bin/sh

python manage.py collectstatic --settings=config.settings.production --noinput

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

gunicorn config.wsgi:application --bind 0.0.0.0:8000 &

daphne -b 0.0.0.0 -p 8001 config.asgi:application &

wait