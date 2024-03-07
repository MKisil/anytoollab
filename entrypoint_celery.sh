#!/bin/sh

chown -R nobody:nogroup /usr/src/app/

celery --workdir=/usr/src/app -A config worker -l INFO --uid=nobody --gid=nogroup