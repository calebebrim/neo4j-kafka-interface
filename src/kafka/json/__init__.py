from confluent_kafka import Producer
import json
import os

def produce(key, value, topic, producer: Producer):
    jvalue = json.dumps(value)
    jkey = json.dumps(key)
    producer.produce(topic=os.environ['B_TOPIC_PREFIX']+topic, value=jvalue, key=jkey)
