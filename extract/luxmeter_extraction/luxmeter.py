import json
import logging
import os
import time
from copy import copy

import requests
from kafka import KafkaProducer

logger = logging.getLogger()
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
LUXMETER_URL = os.environ.get("LUXMETER_URL")
producer = None

rooms = ["kitchen", "bedroom", "bathroom", "living_room"]


def get_luxmeter_data_periodically():
    while (True):
        time.sleep(60)
        get_luxmeter_data()


def get_luxmeter_data():
    for room_id in rooms:
        received_data = requests.get(f'{LUXMETER_URL}{room_id}')
        received_data = received_data.json()
        received_data_json_copy = copy(received_data)
        last_measurement = received_data_json_copy["measurements"][-1]
        received_data_json_copy["measurements"] = last_measurement

        received_data_json_copy.update(
            received_data_json_copy.pop('measurements'))

        record = producer.send('luxmeter', key=room_id.encode(
            'utf-8'), value=received_data_json_copy)
        logger.info(
            f"Luxmeter data sent to Kafka topic successfully: {received_data_json_copy}")


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode('utf8'),
        api_version=(0, 10, 1)
    )
    logging.basicConfig(level=logging.DEBUG)
    get_luxmeter_data_periodically()
