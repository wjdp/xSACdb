FROM wjdp/xsacdb-image:v0.2.0-4 # Remember to update .gitlab-ci.yml too

ADD . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV XSACDB_ENVIRONMENT PRODUCTION
ENV XSACDB_CONTAINER DOCKER

RUN /app/bin/install.sh

CMD /app/bin/run.sh
