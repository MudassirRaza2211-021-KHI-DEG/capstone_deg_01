import json
import logging
import os
import time

import requests
from kafka import KafkaProducer

logger = logging.getLogger()
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda x: json.dumps(x).encode('utf8'),
    api_version=(0, 10, 1)
)

rooms = ["kitchen", "bedroom", "bathroom", "living_room"]


def luxmeter_data():
    while (True):
        time.sleep(60)
        for room_id in rooms:
            received_data = requests.get(
                f'http://sensor:3000/api/luxmeter/{room_id}')
            received_data = received_data.json()
            last_record = f"{received_data['room_id']}: {received_data['measurements'][-1]}"
            record = Producer.send('luxmeter', value=last_record)
            logger.info(f"Received Luxmeter Data: {last_record}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    luxmeter_data()
