#!/bin/bash

cd /app

source env/bin/activate

src/manage.py migrate --noinput
src/manage.py collectstatic --noinput
src/manage.py compress

if [[ $XSACDB_FAKE_DATA = "TRUE" ]]
then
    src/manage.py flush --noinput
    mkdir tmp
    curl $XSACDB_BSAC_DATA > tmp/bsac_data.yaml
    src/manage.py loaddata groups
    src/manage.py loaddata tmp/bsac_data.yaml
    src/manage.py generate_fake_data
fi
