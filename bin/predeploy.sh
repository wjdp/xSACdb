#!/bin/bash

cd /app

if [[ $XSACDB_FAKE_DATA = "TRUE" ]]
then
    echo ">> Development dependencies"
    pipenv install --deploy --system --dev
fi

gulp deploy
src/manage.py collectstatic --noinput
src/manage.py migrate --noinput

if [[ $XSACDB_FAKE_DATA = "TRUE" ]]
then
    mkdir tmp
    curl $XSACDB_BSAC_DATA > tmp/bsac_data.yaml
    src/manage.py reset_fake_db
    for fixture in conf/fixtures/*; do src/manage.py loaddata $fixture; done
fi

src/manage.py setup_scheduler

date +%s > dist/deploy.timestamp
