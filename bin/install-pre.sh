#!/usr/bin/env bash

echo "[xSACdb] Running install-pre.sh"

env

cd /app

echo "[xSACdb] Setting up virtualenv"

rm -rf env
virtualenv env
source env/bin/activate

echo "[xSACdb] Installing python dependencies..."
echo ">> Production dependencies"
pip install -qr requirements.txt

if [[ $XSACDB_FAKE_DATA = "TRUE" ]]
then
    echo ">> Development dependencies"
    pip install -qr requirements_dev.txt
fi

echo "[xSACdb] Installing frontend dependencies..."
# Just check the sass version
sass -v
# Bower things
bower install -q --allow-root
# This folder is trouble (whitenoise issue I think)
rm -rf lib/tether/examples

echo "[xSACdb] install-pre.sh complete!"
