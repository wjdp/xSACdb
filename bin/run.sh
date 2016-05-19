#!/bin/bash

cd /app

source env/bin/activate

src/manage.py migrate --noinput
src/manage.py collectstatic --noinput

gunicorn --chdir src xSACdb.wsgi:application -b 0.0.0.0:5000 -w 4
