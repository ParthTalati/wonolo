FROM python/python:3.7

FROM python/faker

FROM pytest

WORKDIR /app

RUN pip3 install pytest-docker

COPY . /app
