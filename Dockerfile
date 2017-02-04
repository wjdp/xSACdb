FROM wjdp/xsacdb-image:v0.2.0-1

ADD . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV XSACDB_ENVIRONMENT PRODUCTION
ENV XSACDB_CONTAINER DOCKER

RUN /app/bin/install.sh

CMD /app/bin/run.sh
