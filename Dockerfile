FROM python:3.8.3-slim-buster

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y g++ \
    && apt-get install -y postgresql-client && apt-get install -y  postgresql-contrib

COPY . .
RUN chmod 755 tools/wait_for_postgres.sh && \
    chmod 755 tools/run.sh

RUN pip install -r requirements.txt

CMD ["./tools/run.sh"]
