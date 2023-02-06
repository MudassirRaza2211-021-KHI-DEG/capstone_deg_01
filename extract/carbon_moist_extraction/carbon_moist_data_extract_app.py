import json
import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from kafka import KafkaProducer

logger = logging.getLogger()
app = FastAPI()

KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")
Producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda x: json.dumps(x).encode('utf8'),
    api_version=(0, 10, 1)
)


@app.post("/api/fetch/moisturemate_data")
async def collect_moisture_mate_data(request: Request):
    moisturemate_data = await request.json()
    logger.info(f"Received MoistureMate Data: {moisturemate_data}")
    record = Producer.send('moisturemate', value=moisturemate_data)


@app.post("/api/fetch/carbonsense_data")
async def collect_carbonsense_data(request: Request):
    carbonsense_data = await request.json()
    logger.info(f"Received Carbonsense Data: {carbonsense_data}")
    record = Producer.send('carbonsense', value=carbonsense_data)


def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3001)


if __name__ == "__main__":
    run_app()
