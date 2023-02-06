import logging

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()

logger = logging.getLogger()


@app.post("/api/fetch/moisturemate_data")
async def collect_moisture_mate_data(request: Request):
    moisture_mate_received_data = await request.json()
    logger.info(f"Received MoistureMate data: {moisture_mate_received_data}")
    return {"msg": "received moisture_mate data"}


@app.post("/api/fetch/carbonsense_data")
async def collect_carbonsense_data(request: Request):
    carbonsense_received_data = await request.json()
    logger.info(f"Received CarbonSense data: {carbonsense_received_data}")
    return {"msg": "received carbonsense data"}


def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3001)


if __name__ == "__main__":
    run_app()
