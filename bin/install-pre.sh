#!/usr/bin/env bash

echo "[xSACdb] Running install-pre.sh"

env

cd /app

echo "[xSACdb] Installing python dependencies..."

pipenv install --system --deploy

echo "[xSACdb] Installing frontend dependencies..."
# Just check the sass version
sass -v
# NPM things
npm install

mkdir -p dist
date +%s > dist/pre.timestamp

echo "[xSACdb] install-pre.sh complete!"
