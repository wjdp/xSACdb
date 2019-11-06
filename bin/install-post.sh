#!/usr/bin/env bash

set -e
export XSACDB_ALLOW_UNSAFE=TRUE

# Jobs that needs app code here

echo "[xSACdb] Running install-post.sh"

echo "[xSACdb] Setting directory structure"
cd /app

# Make log dir
mkdir log

# Dump the dir, for debugs
pwd
ls -lah

echo "[xSACdb] Frontend build"

npm run build:prod
src/manage.py collectstatic --noinput

echo "[xSACdb] Setting up shell"

cp .bashrc /root/.bashrc
date +%s > dist/post.timestamp

echo "[xSACdb] install-post.sh complete!"
