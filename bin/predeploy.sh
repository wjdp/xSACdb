#!/bin/bash

cd /app

source env/bin/activate

src/manage.py migrate --noinput
src/manage.py collectstatic --noinput
src/manage.py compress

if [[ $XSACDB_FAKE_DATA = "TRUE" ]]
then
    mkdir tmp
    curl $XSACDB_BSAC_DATA > tmp/bsac_data.yaml
    src/manage.py reset_fake_db
    for fixture in conf/fixtures/*; do src/manage.py loaddata $fixture; done
fi
