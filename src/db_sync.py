from src.kafka import get_producer, get_command_consumer
from src.db.neo4j import command_executor

import os
import logging

if os.environ['LOG'] == 'DEB':
    level = logging.DEBUG
elif os.environ['LOG'] == 'INF':
    level = logging.INFO
elif os.environ['LOG'] == 'WAR':
    level = logging.WARN
elif os.environ['LOG'] == 'ERR':
    level = logging.ERROR
else:
    level = logging.INFO


logging.basicConfig(level=level)
logging.info('Initializing n4j commander...')



producer = get_producer()
command_consumer = get_command_consumer()
try:
    while True:
        msg = command_consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        topic = msg.topic()
        offset = msg.offset()
        command = msg.value().decode('utf-8')
        try:
            logging.debug('Command message: {} - (sequence: {})'.format(command, offset))
            command_executor(command)
        except Exception as ex:
            print(ex)



        producer.poll(0)

except Exception as ex:
    print(ex)
    producer.flush()

