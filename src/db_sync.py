from src.kafka import get_producer, iter_messages, fail, respond
from src.db.neo4j import command_executor
import json
import os
import logging




producer = get_producer()

try:
    for msg in iter_messages():
        topic = msg.topic()
        offset = msg.offset()
        message = json.loads(msg.value().decode('utf-8'))
        try:
            text = 'Command message executed: {} - (sequence: {})'.format(message['command'], offset)
            logging.debug(text)
            command_executor(message['command'])
            respond(text)
        except Exception as ex:
            text = "Error while executing command '{}':\n{}".format(message, ex)
            logging.error(text)
            message['error'] = str(ex)
            fail(message=json.dumps(message))

except Exception as ex:
    logging.error("Some exception force the program stop: {}".format(ex))
    producer.flush()

