FROM debian:buster-slim

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

# Locales
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_GB.UTF-8 UTF-8/en_GB.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="en_GB.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_GB.UTF-8
ENV LANG en_GB.UTF-8

# System
RUN apt-get update && apt-get install -qy supervisor build-essential git curl libpq-dev libjpeg-dev zlib1g-dev imagemagick

# Python
RUN apt-get update && apt-get install -qy python3-pip python3-dev
RUN pip3 install pipenv

# Node
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get update && apt-get install -qy nodejs
RUN npm install -g npm

# Ruby
RUN apt-get update && apt-get install -qy ruby ruby-dev
RUN gem install bundler sass

# Application
ENV XSACDB_ENVIRONMENT PRODUCTION
ENV XSACDB_CONTAINER DOCKER

ADD bin/install-pre.sh /app/bin/
ADD Pipfile /app/
ADD Pipfile.lock /app/
ADD package.json /app/
RUN /app/bin/install-pre.sh

ADD . /app
RUN /app/bin/install-post.sh

EXPOSE 5000
CMD /usr/bin/supervisord -c /app/supervisord.conf
