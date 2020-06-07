FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN pytest tests/test_*.py