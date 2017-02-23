![xSACdb](https://raw.githubusercontent.com/wjdp/xSACdb/develop/src/xsd_about/static/images/logo.gif)

[![build status](https://gitlab.com/wjdp/xSACdb/badges/develop/build.svg)](https://gitlab.com/wjdp/xSACdb/commits/develop) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c8831628fa6943f8884c54370e94d87c)](https://www.codacy.com/app/wjdp/xSACdb?utm_source=github.com&utm_medium=referral&utm_content=wjdp/xSACdb&utm_campaign=Badge_Coverage) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/c8831628fa6943f8884c54370e94d87c)](https://www.codacy.com/app/wjdp/xSACdb?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wjdp/xSACdb&amp;utm_campaign=Badge_Grade)

A web based database for managing [BSAC](https://www.bsac.com/) branch clubs. It looks after membership details, training records, known sites and club trips.

Demo
----

You can find information about demo instances of the application here: <http://xsacdb.wjdp.uk/demo/>.

Requirements
------------

- Linux OS, tested on Ubuntu and Debian
- Python 2.7
- virtualenv
- Bower
- Sass

Install
-------
xSACdb is a Python web application, it is built on the Django web framework. For production use the only supported deployment method is via Dokku/Docker. See section below.

Install within a virtualenv container, this isolates the dependencies of xSACdb from the rest of your server. If you know what you're doing this'll get you up and running quickly (config needs doing first):

    bower install
    pip install -r requirements.txt
    src/manage.py migrate
    src/manage.py reset_fake_db
    src/manage.py runserver

You'll also need to run some background task workers with `src/manage.py rqworker` and a scheduler `src/manage.py rqscheduler`.

BSAC Data
---------
The application is distributed without any qualifications, lessons or SDCs. I've not fully looked into this but I'm guessing BSAC has copyright on that data. You'll have to put this in yourself.

Deployment
----------

The only supported deployment method is within a predefined Docker container running on a Dokku server. See http://dokku.viewdocs.io/dokku/ for details about setting up a Dokku server. Run the following on the remote. 

You will need to make a copy of `conf/local_settings.py.example` as `conf/local_settings.py` and define your environment settings and club localisation options.

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
git clone git@gitlab.com:wjdp/xsacdb.git
cd xsacdb
git checkout master
git remote add deploy dokku@YOUR_DOKKU_SERVER:xsacdb
git push deploy master
```
