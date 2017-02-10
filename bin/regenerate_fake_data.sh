#!/bin/bash

source env/bin/activate
rm tmp/db.sqlite3
src/manage.py migrate
src/manage.py loaddata groups
src/manage.py loaddata membershiptypes
src/manage.py loaddata tmp/bsac_data.yaml
src/manage.py generate_fake_data
