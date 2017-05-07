#!/usr/bin/env bash

# Fast stuff / stuff that needs app code here

echo "[xSACdb] Running install-post.sh"

echo "[xSACdb] Setting directory structure"
cd /app

# Make log dir
mkdir log

# Dump the dir, for debugs
pwd
ls -lah

echo "[xSACdb] Setting up shell"

cp .bashrc /root/.bashrc

date +%s > dist/post.timestamp

echo "[xSACdb] install-post.sh complete!"
