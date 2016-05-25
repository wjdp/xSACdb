#!/bin/bash

cd /app

source env/bin/activate

src/manage.py migrate --noinput
src/manage.py collectstatic --noinput
src/manage.py compress

/usr/bin/supervisord
