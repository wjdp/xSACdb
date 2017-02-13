#!/bin/bash

echo ">>> Destroying xSACdb instance xsacdb-$1"

dokku apps:destroy xsacdb-$1
dokku postgres:destroy xsacdb-$1
dokku redis:destroy xsacdb-$1

echo "--------------------------------------------------------------------------------"
echo "App, postgres and redis removed."
echo "Storage remains at /storage/xsacdb/$1"
