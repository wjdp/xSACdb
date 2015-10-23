#!/bin/bash

cd /app

source env/bin/activate

src/manage.py migrate --noinput
src/manage.py collectstatic --noinput

gunicorn --chdir src xSACdb.wsgi:application
