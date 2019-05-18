FROM debian:stretch-slim

RUN apt-get update -qy

RUN apt-get upgrade -qy

# Locales
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_GB.UTF-8 UTF-8/en_GB.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="en_GB.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_GB.UTF-8
ENV LANG en_GB.UTF-8

# System
RUN apt-get install -qy supervisor build-essential git curl libpq-dev \
libjpeg-dev imagemagick

# Python
RUN apt-get install -qy python-virtualenv python-pip python-dev

# Node
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash
RUN apt-get install -qy nodejs
RUN npm install -g bower uglifyjs coffee-script jsonlint gulp-cli

# Ruby
RUN apt-get install -qy ruby ruby-dev
RUN gem install bundler sass

# Application
ENV XSACDB_ENVIRONMENT PRODUCTION
ENV XSACDB_CONTAINER DOCKER

ADD bin/install-pre.sh /app/bin/
ADD requirements.txt /app/
ADD requirements_dev.txt /app/
ADD .bowerrc /app/
ADD bower.json /app/
ADD package.json /app/
RUN /app/bin/install-pre.sh

ADD lib /app/lib
ADD dist /app/dist
ADD . /app
RUN /app/bin/install-post.sh

EXPOSE 5000
CMD /usr/bin/supervisord -c /app/supervisord.conf
