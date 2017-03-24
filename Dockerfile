FROM python:alpine
MAINTAINER sebastian hutter <mail@sebastian-hutter.ch>

ADD build/config/requirements.txt /requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN apk --no-cache add --virtual build-dependencies build-base gcc binutils linux-headers libffi-dev openssl-dev && \
  apk add --no-cache tini libffi && \
  pip install --upgrade -r /requirements.txt && \
  apk del build-dependencies

ADD build/config/uwsgi.ini /uwsgi.ini
ADD build/docker-entrypoint.sh /docker-entrypoint.sh

RUN adduser -D checkhttp \
  && chmod +x /docker-entrypoint.sh

ADD build/app /app

EXPOSE 8080

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/bin/sh", "/docker-entrypoint.sh"]
