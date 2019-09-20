FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y sudo vim build-essential python3-pip python3-dev python3-dev software-properties-common \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install -y wget ca-certificates
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'


RUN apt-get update && apt-get install -y postgresql postgresql-client postgresql-contrib libpq-dev


USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker &&\
    psql --command "CREATE USER wikidata WITH SUPERUSER PASSWORD 'wikidata';" &&\
    psql --command "CREATE DATABASE wikidata;"

EXPOSE 5432

USER root
RUN mkdir -p /opt

WORKDIR /opt

ADD requirements.txt .
RUN python -m pip install --user -r requirements.txt

ADD README.md .
ADD wikimovies.cfg .
ADD wikimovies_main.py .
ADD wikimovies wikimovies

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]








