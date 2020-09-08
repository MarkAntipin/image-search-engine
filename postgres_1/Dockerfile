FROM postgres:12

RUN apt-get update && apt-get install -y build-essential curl postgresql-server-dev-12
RUN curl https://ftp.postgresql.org/pub/source/v12.0/postgresql-12.0.tar.bz2 -o /postgresql-12.0.tar.bz2
RUN cd / && tar xvf postgresql-12.0.tar.bz2
RUN cd /postgresql-12.0/contrib/cube && sed -i 's/#define CUBE_MAX_DIM (100)/#define CUBE_MAX_DIM (512)/' cubedata.h && \
    USE_PGXS=true make && USE_PGXS=true make install

RUN apt install -y git && git clone git://sigaev.ru/smlar.git && cd smlar && USE_PGXS=true make \
    && USE_PGXS=true make install
