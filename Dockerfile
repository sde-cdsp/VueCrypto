FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir /vuecrypto
WORKDIR /vuecrypto
COPY requirements.txt /vuecrypto/

RUN apk add g++ \
    && apk add postgresql-dev  \
    && pip install -r requirements.txt



