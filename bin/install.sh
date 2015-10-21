#!/bin/bash

echo "[xSACdb] Checking directory structure"
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

echo "[xSACdb] Installing python dependancies..."
pip install -q -r requirements.txt

echo "[xSACdb] Installing frontend dependancies..."
bower install -q --allow-root

echo "[xSACdb] Migrating database..."
# src/manage.py migrate --noinput

echo "[xSACdb] Collecting static files..."
# src/manage.py collectstatic --noinput
