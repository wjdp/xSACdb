![xSACdb](https://raw.githubusercontent.com/wjdp/xSACdb/develop/src/xsd_about/static/images/logo.gif)

A web based database for managing BSAC branch clubs. It looks after membership details, training records, known sites, kit and club trips.

Current Limitations
-------------------
- **Trips** are not implemented
- **Kit** is not implemented
- **Sites** is rather basic

- Most of the other bits are still in active development. The project is in production use as of September 2014 in a single club, in 2016 additional clubs started deploying the product.
- The application incorporates Facebook login in addition to local accounts. This, at this time, can't be easily disabled.

Install
-------
xSACdb is a Python web application, it is built on the Django web framework. Its runs on Linux servers. You'll also need a Postgres and Redis servers. A better alternative offering quicker install and rapid upgrades is using Docker/dokku, see section below.

If you're unfamiliar with running Python web services have a read up on those first. xSACdb runs it's own web server which you then proxy access to using Apache/Nginx or some other public facing web server. You'll need to serve static files with your own web server.

You will need to make a copy of `conf/local_settings.py.example` as `conf/local_settings.py` and define your environment settings and club localisation options. In order to specify production XSACDB_ENVIRONMENT should be set to PRODUCTION.

Install within a virtualenv container, this isolates the dependencies of xSACdb from the rest of your server. If you know what you're doing this'll get you up and running quickly (config needs doing first):

    pip install -r requirements.txt
    ./manage.py compress
    ./manage.py collectstatic
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

You'll also need to run some background task workers with `src/manage.py rqworker` and a scheduler `src/manage.py rqscheduler`.

It is advised to have a read through of the deployment checklist: https://docs.djangoproject.com/en/dev/howto/deployment/checklist/ before providing public access to the application.

BSAC Data
---------
The application is distributed without any qualifications, lessons or SDCs. I've not fully looked into this but I'm guessing BSAC has copyright on that data. You'll have to put this in yourself.

Dokku Config
------------

An alternative to building the environment needed to run the application is to run it within a predefined Docker container. See http://dokku.viewdocs.io/dokku/ for details about setting up a Dokku server. Run the following on the remote, add config files to `/storage/xsacdb/conf`.

```
dokku apps:create xsacdb
dokku plugin:install https://github.com/dokku/dokku-postgres.git
dokku postgres:create xsacdb
dokku postgres:link xsacdb xsacdb
dokku plugin:install https://github.com/dokku/dokku-redis.git redis
dokku redis:create xsacdb
dokku redis:link xsacdb xsacdb
mkdir -p /storage/xsacdb/conf /storage/xsacdb/media
dokku storage:mount xsacdb /storage/xsacdb/conf/:/app/conf/
dokku storage:mount xsacdb /storage/xsacdb/media/:/app/media/
```

Now on your local machine: obtain the code, add your dokku server as a git remote, and push to deploy.

```
git clone git@git.fullaf.com:wjdp/xsacdb.git
cd xsacdb
git checkout master
git remote add deploy dokku@YOUR_DOKKU_SERVER:xsacdb
git push deploy master
```
