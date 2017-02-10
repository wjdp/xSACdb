#!/bin/bash

echo ">>> Creating xSACdb instance xsacdb-$1"

dokku apps:create xsacdb-$1

echo ">>> Creating and linking postgres and redis instances"

dokku postgres:create xsacdb-$1
dokku postgres:link xsacdb-$1 xsacdb-$1
dokku redis:create xsacdb-$1
dokku redis:link xsacdb-$1 xsacdb-$1

echo ">>> Creating and linking storage"

sudo mkdir -p /storage/xsacdb/$1/conf/static /storage/xsacdb/$1/media
sudo chown -R dokku:dokku /storage/xsacdb/$1
dokku storage:mount xsacdb-$1 /storage/xsacdb/$1/conf/:/app/conf/
dokku storage:mount xsacdb-$1 /storage/xsacdb/$1/media/:/app/media/
