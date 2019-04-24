#!/usr/bin/env bash

export $(cat variables.env | xargs)

docker network create crypto-net

# Postgres database mounted in db_data
docker run --rm -d \
           --name db \
           --volume db_data:/var/lib/postgresql/data \
           --network crypto-net \
           -e POSTGRES_PASSWORD=${DOCKER_DB_PWD} -e POSTGRES_DB=${DOCKER_DB_NAME} -e POSTGRES_USER=${DOCKER_DB_USER} \
           postgres

# Django application
docker run --rm \
           --name django \
           --network crypto-net -p 8000:80 \
           --volume $(pwd):/cryptodjango \
           --entrypoint ./entrypoint.sh \
           -e DOCKER_DB_PWD -e DOCKER_DB_NAME -e DOCKER_DB_USER -e DOCKER_DB_PORT -e DOCKER_DB_HOST -e DOCKER_DB_ENGINE -e DOCKER_SECRET_KEY \
           littletoof/mycryptolist-django:latest

# Vue application
docker run --rm -d \
           --name vue \
           --network crypto-net -p 8001:8001 \
           --volume $(pwd)/mycryptolist:/cryptovue \
           littletoof/mycryptolist-vue:latest \
           npm run serve
