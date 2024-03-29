FROM python:3.6.10-buster

RUN python3 -m pip install confluent-kafka neo4j deprecation
COPY src /service/src
WORKDIR /service

ENTRYPOINT [ "/bin/sh"]
