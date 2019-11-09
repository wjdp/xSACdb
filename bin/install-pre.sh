#!/usr/bin/env bash

set -e

echo "[xSACdb] Running install-pre.sh"

env

cd /app

echo "[xSACdb] Installing python dependencies..."

pipenv install --system --deploy

echo "[xSACdb] Installing frontend dependencies..."

npm ci --production
mkdir -p dist
date +%s > dist/pre.timestamp

echo "[xSACdb] install-pre.sh complete!"
