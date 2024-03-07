FROM python:3.12.0-alpine3.18

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    gcc \
    python3-dev \
    libc-dev \
    linux-headers

RUN apk add postgresql-client build-base postgresql-dev

COPY ./config ./config
COPY ./requirements ./requirements
COPY ./src ./src
COPY ./.env .
COPY ./.env_dev .
COPY ./entrypoint.sh .
COPY ./entrypoint_celery.sh .
COPY ./entrypoint_celery_beats.sh .
COPY ./manage.py .

RUN pip install -r ./requirements/production.txt

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]