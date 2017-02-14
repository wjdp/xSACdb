# Remember to update .gitlab-ci.yml too
FROM wjdp/xsacdb-image:v0.2.0-4

ENV XSACDB_ENVIRONMENT PRODUCTION
ENV XSACDB_CONTAINER DOCKER

ADD . /app

RUN /app/bin/install.sh

CMD /usr/bin/supervisord -c /app/supervisord.conf
