# syntax=docker/dockerfile:experimental
FROM python:3.8.3-slim-buster

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y g++ \
    && apt-get install -y postgresql-client && apt-get install -y  postgresql-contrib \
    && apt-get install -y wget && wget -c https://download.pytorch.org/models/alexnet-owt-4df8aa71.pth

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip \
        pip install fastapi python-multipart python-dotenv uvicorn \
        hnswlib img2vec-pytorch tortoise-orm asyncpg filetype aiofiles \
        ujson
