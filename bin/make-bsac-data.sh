#!/bin/sh
src/manage.py dumpdata --format yaml xsd_training.Lesson xsd_training.Qualification xsd_training.SDC > ../bsac-data/bsac_data.yaml
