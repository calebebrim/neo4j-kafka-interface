
from src.kafka import get_producer, iter_messages, respond, fail
from src.db.neo4j import query_executor
import logging
import json


producer = get_producer()

try:
    for msg in iter_messages():

        topic = msg.topic()
        offset = msg.offset()
        query = json.loads(msg.value().decode('utf-8'))
        try:
            query_command: str = query['execute']
            if query_command.startswith('MATCH('):
                raise Exception("Query commands must start with MATCH word.")
            logging.debug('Query message: {} - (sequence: {})'.format(query_command, offset))
            for result in query_executor(query_command):
                result_obj = {}
                
                result_obj['properties'] = dict(result)
                text = json.dumps(result_obj)
                logging.debug(text)
                query['result'] = result_obj
                respond(json.dumps(query), to=query['to'])

        except Exception as ex:
            query['error'] = str(ex)
            fail(message=json.dumps(query))

except Exception as ex:
    logging.error(ex)
    producer.flush()

