#!/bin/bash

# Local test suite

source env/bin/activate
coverage run --include=src/* --omit=*/migrations/*  src/manage.py test xSACdb xsd_about xsd_auth xsd_frontend xsd_help xsd_kit xsd_members xsd_sites xsd_training xsd_trips
mkdir -p tmp/
coverage html -d tmp/htmlcov
xdg-open tmp/htmlcov/index.html
