#!/bin/sh

celery --workdir=/usr/src/app -A config worker -l INFO