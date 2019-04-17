#!/usr/bin/env bash

export $(cat variables.env | xargs)

docker network create crypto-net

# Postgres database mounted in db_data
docker run --rm -d \
           --name db \
           --volume db_data:/var/lib/postgresql/data \
           --network crypto-net \
           -e POSTGRES_PASSWORD -e POSTGRES_DB -e POSTGRES_USER \
           postgres

# Django application
docker run --rm -d \
           --name cryptodjango \
           --network crypto-net -p 8000:80 \
           --volume $(pwd):/vuecrypto \
           --entrypoint ./entrypoint.sh \
           -e POSTGRES_PASSWORD -e POSTGRES_DB -e POSTGRES_USER \
           django_image:latest

# vue application
docker run --rm \
           --name cryptovue \
           --network crypto-net -p 8001:8001 \
           --volume $(pwd)/mycryptolist:/mycryptolist \
           vue_image:latest \
           npm run serve
