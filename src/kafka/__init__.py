from confluent_kafka import Producer, Consumer, Message

from src.kafka.string import subscribe
import json
import logging
import os


def get_producer() -> Producer:
    logging.info('Initializing Producer')
    producer = Producer(get_producer_properties())
    return producer


def handle_requests(function: object):
    for message in iter_requests():
        function(message)


def iter_requests() -> Message:
    try:
        requester = get_requests_consumer()

        while True:
            msg = requester.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                logging.error("Consumer error: {}".format(msg.error()))
                continue
            yield msg

    except Exception as ex:
        logging.error(ex)


def get_requests_consumer() -> Consumer:
    c = Consumer(get_consumer_properties(
        mode='latest'))
    subscribe([os.environ['REQUEST_TOPIC']], consumer=c)
    return c


def request_string_responder(value: str):
    producer = get_producer()
    producer.produce(topic=os.environ['RESPONSE_TOPIC'], value=value)
    producer.poll(0)
    producer.flush()


def get_responser_producer() -> Producer:
    return get_producer()


def get_command_consumer() -> Consumer:
    logging.info('Initializing Consumer')
    c = Consumer(get_consumer_properties())
    subscribe([os.environ['REQUEST_TOPIC']], consumer=c, offset=0)
    return c


def get_consumer_properties(mode: str = 'smallest'):
    if 'B_USERNAME' in os.environ:
        prop = {
            'bootstrap.servers': os.environ['BROKERS'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': mode},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.environ['B_USERNAME'],
            'sasl.password': os.environ['B_PASSWORD'],
            'group.id': os.environ['GROUP_ID'],
        }
    else:
        prop = {
            'bootstrap.servers': os.environ['BROKERS'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': mode},
            'group.id': os.environ['GROUP_ID'],
        }
    logging.info('Consumer Properties: {}'.format(json.dumps(prop,indent=4,sort_keys=True)))
    return prop


def get_producer_properties() -> dict:
    if 'B_USERNAME' in os.environ:
        prop = {
            'bootstrap.servers': os.environ['BROKERS'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': os.environ['B_USERNAME'],
            'sasl.password': os.environ['B_PASSWORD'],
            'group.id': os.environ['GROUP_ID']
        }
    else:
        prop = {
            'bootstrap.servers': os.environ['BROKERS'],
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'group.id': os.environ['GROUP_ID']
        }
    logging.info('Producer Properties: {}'.format(json.dumps(prop,indent=4,sort_keys=True)))
    return prop
