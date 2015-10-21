#!/bin/bash

cd /app
pwd
ls -lah

echo "/app/conf"
ls -lah /app/conf

echo "/app/media"
ls -lah /app/media

rm -rf env

virtualenv env

source env/bin/activate

echo "Installing python dependancies..."
pip install -q -r requirements.txt

echo "Installing frontend dependancies..."
bower install -q --allow-root

mkdir tmp

src/manage.py migrate --noinput
src/manage.py collectstatic --noinput
