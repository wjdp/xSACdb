![xSACdb](https://raw.github.com/wjdp/xSACdb/master/static/images/logo.gif)

A web based database for managing BSAC branch clubs. It looks after membership details, training records, known sites and club trips.

Current Issues
--------------
- **Trips** are not implemented
- **Sites** are rather basic
- **Training** still needs some of the admin features (managing qualifictions etc)
- The **auth** system currently doesn't accept username based signups, I would like to have email based login too.

Install
-------
xSACdb is a Python web application, it is built on the Django web framework. You can run it on any Linux/Mac and even Windows based system. You'll also need a MySQL or Postgres database server.

If you're unfamilier with running Python web services have a read up on those first. xSACdb runs it's own web server which you then proxy access to using Apache/Nginx or some other public facing web server. You'll need to serve static files with your own web server.

I recommend installing in a virtualenv container, this isolates the depenancies of xSACdb from the rest of your server. If you know what you're doing this'll get you up and running quickly (config needs doing first):

    pip install -r requirements.txt
    ./manage.py syncdb  # Don't add a superuser now!
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver
    
Deployment Caveats
------------------
You need to overwrite the default config in xSACdb, firstly if deploying publically ensure DEBUG is set to False. Then have a read through of the deployement checklist: https://docs.djangoproject.com/en/dev/howto/deployment/checklist/.

It would be very nice for xSACdb to do this for you, it's on the to do list!


