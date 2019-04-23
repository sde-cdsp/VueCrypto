FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir /cryptodjango
WORKDIR /cryptodjango
COPY requirements.txt /cryptodjango/

RUN apk add g++ \
    && apk add postgresql-dev  \
    && pip install -r requirements.txt




