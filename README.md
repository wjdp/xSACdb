![xSACdb](https://raw.githubusercontent.com/wjdp/xSACdb/master/assets/images/xsacdb.gif)

[![build status](https://gitlab.com/wjdp/xSACdb/badges/master/build.svg)](https://gitlab.com/wjdp/xSACdb/commits/master) ![coverage](https://gitlab.com/wjdp/xSACdb/badges/master/coverage.svg)

A web based database for managing [BSAC](https://www.bsac.com/) branch clubs. It looks after membership details, training records, known sites and club trips.

![xSACdb Screenshot](https://raw.githubusercontent.com/wjdp/xSACdb/master/assets/screenshots/dashboard.png)

Demo
----

You can find information about demo instances of the application here: <http://xsacdb.wjdp.uk/demo/>.


Requirements
------------

- Linux OS, tested on Ubuntu and Debian
- Python 3.7
- Node 12.x
- pipenv


Running Locally
-------
xSACdb is a Python web application, it is built on the Django web framework. For production use the only supported deployment method is via Docker. See section below.

For development you can run the server from a local shell. Firstly get your local environment set up by installing Python and frontend packages:

    npm install
    pipenv install

Then get your database created and filled with fake data:

    pipenv run src/manage.py migrate
    pipenv run src/manage.py reset_fake_db

Finally start the application with:

    pipenv run honcho start


BSAC Data
---------
The application is distributed without any qualifications, lessons or SDCs. I've not fully looked into this but I'm guessing BSAC has copyright on that data. You'll have to put this in yourself.


Deployment
----------

Deployment is via a docker container. See the `docker-compose.yml` file in the repo for an example on how to get a server up. More docs to follow.
