#!/bin/sh

chown -R nobody:nogroup /usr/src/app/
mkdir -p /usr/src/app/media/
chmod -R u+rwX,go+rX,go-w /usr/src/app/media/

celery --workdir=/usr/src/app -A config worker -l INFO --uid=nobody --gid=nogroup