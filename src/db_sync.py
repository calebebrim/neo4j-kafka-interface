
from src.kafka import get_producer, get_command_consumer
from src.db.neo4j import command_executor
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
            print('Command message: {} - (sequence: {})'.format(command, offset))
            command_executor(command)
        except Exception as ex:
            print(ex)



        producer.poll(0)

except Exception as ex:
    print(ex)
    producer.flush()

