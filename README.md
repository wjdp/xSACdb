![xSACdb](https://raw.githubusercontent.com/wjdp/xSACdb/develop/src/xsd_about/static/images/logo.gif)

A web based database for managing BSAC branch clubs. It looks after membership details, training records, known sites, kit and club trips.

Current Limitations
-------------------
- **Trips** are not implemented
- **Kit** is not implemented
- **Sites** is rather basic

- Most of the other bits are still in active development. The project is in production use as of September 2014 in a single club, this is being used to iron out problems with the implementation. The hope is to have a well rounded system by summer 2015. Releases for this club are tagged as nu-x.

- The application incorporates Facebook login in addition to local accounts. This, at this time, can't be easily disabled.

- SASS files don't have a nice generation script

Install
-------
xSACdb is a Python web application, it is built on the Django web framework. You can run it on any Linux/Mac and even Windows based system. You'll also need a MySQL or Postgres database server.

If you're unfamiliar with running Python web services have a read up on those first. xSACdb runs it's own web server which you then proxy access to using Apache/Nginx or some other public facing web server. You'll need to serve static files with your own web server.

I recommend installing in a virtualenv container, this isolates the dependencies of xSACdb from the rest of your server. If you know what you're doing this'll get you up and running quickly (config needs doing first):

Stick bourbon in `vendor/bourbon`

	sass --watch xsd_frontend/static/sass/login.sass:xsd_frontend/static/cssb/login.css --load-path .
    pip install -r requirements.txt
    ./manage.py collectstatic
    ./manage.py syncdb  # Don't add a superuser now!
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

You will need to make a copy of `local_settings.py.example` as `local_settings.py` and define your environment settings and club localisation options.

It is advised to have a read through of the deployment checklist: https://docs.djangoproject.com/en/dev/howto/deployment/checklist/ before providing public access to the application.

BSAC Data
---------
The application is distributed without any qualifications, lessons or SDCs. I've not fully looked into this but I'm guessing BSAC has copyright on that data. You'll have to put this in yourself.

dokku Config
------------

```
dokku apps:create xsacdb
dokku plugin:install https://github.com/dokku/dokku-postgres.git
dokku postgres:create xsacdb
dokku postgres:link xsacdb xsacdb
dokku storage:mount xsacdb /storage/xsacdb/conf/:/app/conf/
dokku storage:mount xsacdb /storage/xsacdb/media/:/app/media/
```
