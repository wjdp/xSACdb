#!/bin/bash

cd /app

source env/bin/activate

gunicorn --chdir src xSACdb.wsgi:application
