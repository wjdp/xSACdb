#!/bin/bash

cd /app
pwd
ls

rm -rf env

virtualenv env

source env/bin/activate

pip install -q -r requirements.txt

bower install -q --allow-root

cp src/local_settings.py.example src/local_settings.py

mkdir tmp

src/manage.py migrate --noinput
src/manage.py collectstatic --noinput
