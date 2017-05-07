#!/bin/bash

cd /app

source env/bin/activate

if [[ $XSACDB_FAKE_DATA = "TRUE" ]]
then
    echo ">> Development dependencies"
    pip install -qr requirements_dev.txt
fi

src/manage.py migrate --noinput
gulp deploy
src/manage.py collectstatic --noinput

if [[ $XSACDB_FAKE_DATA = "TRUE" ]]
then
    mkdir tmp
    curl $XSACDB_BSAC_DATA > tmp/bsac_data.yaml
    src/manage.py reset_fake_db
    for fixture in conf/fixtures/*; do src/manage.py loaddata $fixture; done
fi

src/manage.py setup_scheduler

date +%s > dist/deploy.timestamp
