#!/bin/bash

# Development server

gunicorn --reload --chdir src xSACdb.wsgi:application
