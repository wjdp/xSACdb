#!/bin/bash

echo "[xSACdb] Ensure needed packages are installed"
apt-get install -qqy python-pip python-dev supervisor ruby-dev nodejs npm imagemagick wget libpq-dev libjpeg-dev \
    libjpeg8-dev supervisor
gem install sass -q

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
pip install -qr requirements.txt

echo "[xSACdb] Installing frontend dependancies..."
sass -v
bower install -q --allow-root
rm -rf lib/tether/examples

echo "[xSACdb] install.sh complete!"
