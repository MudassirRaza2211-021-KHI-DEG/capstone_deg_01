import logging

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/api/collect/moisturemate_data")
async def collect_moisture_mate_data(request: Request):
    received_data = await request.json()
    print(f"Received MoistureMate Data: {received_data}")
    return {"msg": "received moisture_mate data"}


@app.post("/api/collect/carbonsense_data")
async def collect_carbonsense_data(request: Request):
    received_data = await request.json()
    print(f"Received carbonsense Data: {received_data}")
    return {"msg": "received carbonsense data"}


def run_app():
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3001)


if __name__ == "__main__":
    run_app()
