FROM python:2.7.11

MAINTAINER Jacob Zelek <jacob.zelek@gmail.com>

ENV KEYS /config.json

COPY . /
WORKDIR /

RUN apt-get update
RUN apt-get install -y nginx supervisor
RUN pip install uwsgi
RUN pip install -r requirements.txt

RUN \
  echo "daemon off;" >> /etc/nginx/nginx.conf \
  && rm /etc/nginx/sites-enabled/default \
  && ln -s /nginx.conf /etc/nginx/sites-enabled/ \
  && ln -s /supervisor.conf /etc/supervisor/conf.d/

EXPOSE 80
CMD ["supervisord", "-n"]