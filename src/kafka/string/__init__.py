from confluent_kafka import Producer, Consumer
import os


def produce(key:str, value:str, topic:str , producer: Producer):
    producer.produce(topic=os.environ['B_TOPIC_PREFIX']+topic, value=value, key=key)


def subscribe(topics: list, consumer: Consumer, offset: int = None):
    topics = list(map(lambda topic: os.environ['B_TOPIC_PREFIX']+topic, topics))

    if offset:
        def on_assign(consumer, partitions):
            for p in partitions:
                p.offset = offset
        consumer.subscribe(topics, on_assign=on_assign)
    else:
        consumer.subscribe(topics)
