from datetime import datetime
from confluent_kafka import Producer, KafkaException
import json
from fastapi import HTTPException
import os

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

kafka_config = {
    "bootstrap.servers": f"{KAFKA_HOST}:{KAFKA_PORT}",
}
producer = Producer(kafka_config)
def generate_event_data(user: int, email: str, action: str,) -> dict:
    return {
        'user': user,
        'email': email,
        'action': action,
        'timestamp': datetime.utcnow().isoformat()
    }

def create_kafka_producer():

    config = {
        'bootstrap.servers': f"{KAFKA_HOST}:{KAFKA_PORT}",
        'client.id': 'user-service'
    }
    producer = Producer(config)
    return producer

def send_event(producer: Producer, event_data: dict):
    try:
        message = json.dumps(event_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serializing event data: {str(e)}")

    topic = KAFKA_TOPIC

    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.flush()