![xSACdb](https://raw.githubusercontent.com/wjdp/xSACdb/develop/src/xsd_about/static/images/logo.gif)

[![build status](https://gitlab.com/wjdp/xSACdb/badges/develop/build.svg)](https://gitlab.com/wjdp/xSACdb/commits/develop) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c8831628fa6943f8884c54370e94d87c)](https://www.codacy.com/app/wjdp/xSACdb?utm_source=github.com&utm_medium=referral&utm_content=wjdp/xSACdb&utm_campaign=Badge_Coverage) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/c8831628fa6943f8884c54370e94d87c)](https://www.codacy.com/app/wjdp/xSACdb?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wjdp/xSACdb&amp;utm_campaign=Badge_Grade)

A web based database for managing [BSAC](https://www.bsac.com/) branch clubs. It looks after membership details, training records, known sites and club trips.

Demo
----

You can find information about demo instances of the application here: <http://xsacdb.wjdp.uk/demo/>.

Requirements
------------

- Linux OS, tested on Ubuntu and Debian
- Python 3.7
- Node 12.x
- virtualenv
- Sass

Install
-------
xSACdb is a Python web application, it is built on the Django web framework. For production use the only supported deployment method is via Docker. See section below.

Install within a virtualenv container, this isolates the dependencies of xSACdb from the rest of your server. If you know what you're doing this'll get you up and running quickly (config needs doing first):

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

Deployment via Dokku is no longer supported. See the `docker-compose.yml` file in the repo for an example on how to get a server up. More docs to follow.
