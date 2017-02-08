#!/bin/bash

sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt:cron-job --add
sudo dokku plugin:install https://github.com/dokku/dokku-maintenance.git
