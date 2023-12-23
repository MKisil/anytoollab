FROM python:3.12.0-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    gcc \
    python3-dev \
    libc-dev \
    linux-headers

COPY requirements /temp/requirements
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements/local.txt

WORKDIR /myproject

COPY . .

EXPOSE 8000
