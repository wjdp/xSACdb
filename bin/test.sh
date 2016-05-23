#!/bin/bash

# Local test suite

source env/bin/activate
src/manage.py validate
src/manage.py check
src/manage.py compress
src/manage.py collectstatic --noinput
src/manage.py test xSACdb xsd_about xsd_auth xsd_frontend xsd_help xsd_kit xsd_members xsd_sites xsd_training xsd_trips
