import json
import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from kafka import KafkaProducer

logger = logging.getLogger()
app = FastAPI()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")

producer = None


@app.post("/api/fetch/moisturemate_data")
async def collect_moisture_mate_data(request: Request):
    moisturemate_data = await request.json()
    logger.info(f"Received MoistureMate Data: {moisturemate_data}")
    record = producer.send('moisturemate', key=(
        moisturemate_data['room_id']).encode('utf-8'), value=moisturemate_data)
    logger.debug(
        f"Moisturemate data sent to Kafka topic successfully: {record}")


@app.post("/api/fetch/carbonsense_data")
async def collect_carbonsense_data(request: Request):
    carbonsense_data = await request.json()
    logger.info(f"Received Carbonsense Data: {carbonsense_data}")
    record = producer.send('carbonsense', key=(
        carbonsense_data['room_id']).encode('utf-8'), value=carbonsense_data)
    logger.debug(
        f"Carbonsense data sent to Kafka topic successfully: {record}")


def run_app():
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=3001)


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode('utf8'),
        api_version=(0, 10, 1)
    )
    run_app()
