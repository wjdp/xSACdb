# Remember to update .gitlab-ci.yml too
FROM wjdp/xsacdb-image:v0.4.0-1

ENV XSACDB_ENVIRONMENT PRODUCTION
ENV XSACDB_CONTAINER DOCKER

ADD bin/install-pre.sh /app/bin/
ADD requirements.txt /app/
ADD requirements_dev.txt /app/
ADD .bowerrc /app/
ADD bower.json /app/
ADD package.json /app/
RUN /app/bin/install-pre.sh

ADD . /app
RUN /app/bin/install-post.sh

CMD /usr/bin/supervisord -c /app/supervisord.conf
