#!/bin/bash

echo "[xSACdb] Setting up shell"
cp /app/.bashrc /root/.bashrc

echo "[xSACdb] Checking directory structure"
cd /app
mkdir log

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
