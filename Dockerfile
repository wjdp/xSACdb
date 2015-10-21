FROM wjdp/flatcar

ADD . app

RUN /app/bin/install.sh

EXPOSE 8000

CMD /app/bin/run.sh
