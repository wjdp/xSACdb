FROM wjdp/flatcar

RUN virtualenv env

RUN source env/bin/activate

RUN pip install -r requirements.txt

RUN bower install --allow-root

RUN cp src/local_settings.py.example src/local_settings.py

RUN mkdir tmp

RUN src/manage.py migrate
RUN src/manage.py collectstatic

CMD src/runserver 0.0.0.0:80
