
from src.kafka import get_producer, iter_requests, request_string_responder
from src.db.neo4j import query_executor
import os
producer = get_producer()


try:

    for msg in iter_requests():

        topic = msg.topic()
        offset = msg.offset()
        command = msg.value().decode('utf-8')
        try:
            print('Query message: {} - (sequence: {})'.format(command, offset))

            for result in query_executor(command):
                print(result)
                request_string_responder(str(result))


            # producer.produce()
        except Exception as ex:
            print(ex)







except Exception as ex:
    print(ex)
    producer.flush()

