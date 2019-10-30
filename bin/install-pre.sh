#!/usr/bin/env bash

echo "[xSACdb] Running install-pre.sh"

env

cd /app

echo "[xSACdb] Installing python dependencies..."

pipenv install --system --deploy

echo "[xSACdb] Installing frontend dependencies..."
# Just check the sass version
sass -v
# Bower things
bower install -q --allow-root
# This folder is trouble (whitenoise issue I think)
rm -rf lib/tether/examples
# NPM things
npm install

mkdir -p dist
date +%s > dist/pre.timestamp

echo "[xSACdb] install-pre.sh complete!"
