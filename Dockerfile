# syntax=docker/dockerfile:experimental
FROM python:3.8.3-slim-buster

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y g++ \
    && apt-get install -y postgresql-client && apt-get install -y  postgresql-contrib

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip \
        pip install fastapi python-multipart python-dotenv uvicorn \
        hnswlib img2vec-pytorch filetype aiofiles \
        ujson sqlalchemy psycopg2-binary
