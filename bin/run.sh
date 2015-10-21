#!/bin/bash

cd /app

source env/bin/activate

src/manage.py runserver 0.0.0.0:8000
