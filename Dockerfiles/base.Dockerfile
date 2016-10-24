FROM python:3.5-alpine

WORKDIR /usr/src/pyfes

COPY . .

RUN apk --no-cache add --virtual build-dependencies \
        build-base \
        libxml2-dev \
        libxslt-dev \
    && apk --no-cache add \
        libxslt \
        libxml2 \
    && pip install --requirement requirements/base.txt \
    && pip install . \
    && apk del build-dependencies
