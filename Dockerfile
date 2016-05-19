FROM wjdp/flatcar

ADD . /app

ENV XSACDB_ENVIRONMENT PRODUCTION
ENV XSACDB_CONTAINER DOCKER

RUN /app/bin/install.sh

CMD /app/bin/run.sh
