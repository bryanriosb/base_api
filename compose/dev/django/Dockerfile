FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps curl gcc libc-dev g++ libffi-dev libxml2 python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \
  # Required to PyODBC \
  && curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_amd64.apk \
  && apk add --allow-untrusted msodbcsql18_18.3.2.1-1_amd64.apk \
  && apk add unixodbc-dev \
  && apk add unixodbc \
  && apk add libpq-dev libssl3 libcrypto3 \
  && apk add openssl \
  && rm -rf /var/cache/apk/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip setuptools && \
    # Required because standard wheels not numpy compile on alpine.
    pip install --extra-index-url https://alpine-wheels.github.io/index numpy==1.23.5 && \
    pip install -r /requirements/dev.txt

COPY ./compose/dev/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/dev/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/dev/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/dev/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
