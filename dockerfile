FROM python:3.6.10-buster
# FROM ubuntu:16.04

# RUN chmod -rwxr-xr-x .

# RUN apt-get update

# RUN apt-get install -y build-essential python3 python3-pip 

# update pip
# RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install confluent-kafka neo4j
COPY src /service/src
WORKDIR /service

ENTRYPOINT [ "/bin/sh" ]
