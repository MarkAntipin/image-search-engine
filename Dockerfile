# syntax=docker/dockerfile:experimental
FROM python:3.8.3-slim-buster

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y g++ \
    && apt-get install -y postgresql-client && apt-get install -y  postgresql-contrib

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8001"]