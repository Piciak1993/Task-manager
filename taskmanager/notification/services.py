from confluent_kafka import Consumer
import json
from threading import Thread
import os

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = int(os.getenv('KAFKA_PORT', '9092'))

task_notifications_store = []


consumer_config = {
    'bootstrap.servers': f"{KAFKA_HOST}:{KAFKA_PORT}",
    'group.id': 'notification-service',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)

def consume_events():
    consumer.subscribe([KAFKA_TOPIC])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Kafka error: {msg.error()}")
            continue


        event_data = json.loads(msg.value().decode('utf-8'))
        task_notifications_store.append(event_data)
        print(f"Received event: {event_data}")

def start_kafka_consumer():
    consume_events()


thread = Thread(target=start_kafka_consumer, daemon=True)
thread.start()