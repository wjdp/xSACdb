#!/bin/bash

echo ">>> Add domain $2 to xsacdb-$1"
dokku domains:add xsacdb-$1 $2
echo ">>> Set email $3 for xsacdb-$1"
dokku config:set --no-restart xsacdb-$1 DOKKU_LETSENCRYPT_EMAIL=$3
echo ">>> Get certs"
dokku letsencrypt xsacdb-$1
