import asyncio
import logging
import os
import random
from csv import DictReader
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict

import httpx
import pandas as pd

logger = logging.getLogger()


@dataclass
class Measurement:
    temperature: float
    humidity: float
    humidity_ratio: float
    light: float
    co2: float


class SensorService:
    def __init__(self):
        self._moisture_mate_url = os.environ.get("MOISTURE_MATE_URL")
        self._carbon_sense_url = os.environ.get("CARBON_SENSE_URL")
        self._smart_thermo_bucket = os.environ.get("SMART_THERMO_BUCKET")

        if None in (
            self._moisture_mate_url,
            self._carbon_sense_url,
            self._smart_thermo_bucket,
        ):
            msg = "You need to specify SMART_THERMO_BUCKET, MOISTURE_MATE_URL and CARBON_SENSE_URL"
            logger.error(msg)
            raise Exception(msg)

        self.positive_samples = self._read_file("positive.csv")
        self.negative_samples = self._read_file("negative.csv")

        self.data: Dict[str, Dict[str, Measurement]] = {}
        self.change_room_cooldown = 0
        self.occupied_room = None
        self.rooms = ["kitchen", "bedroom", "bathroom", "living_room"]

    async def start(self):
        asyncio.create_task(self._loop())

    async def save_smart_thermo(self, date: str, sample: Dict[str, Measurement]):
        df = pd.DataFrame(
            [
                {
                    "timestamp": date,
                    "room_id": room,
                    "temperature": measurement.temperature,
                }
                for room, measurement in sample.items()
            ]
        )

        df.to_csv(f"s3://{self._smart_thermo_bucket}/smart_thermo/{date}.csv")

    async def send_moisture_mate(self, date: str, sample: Dict[str, Measurement]):
        for room, measurement in sample.items():
            data = {
                "timestamp": date,
                "room_id": room,
                "humidity": measurement.humidity,
                "humidity_ratio": measurement.humidity_ratio,
            }

            await self._send_request(self._moisture_mate_url, data)

            logger.info(f"MoistureMate: {data} sent to {self._moisture_mate_url}")

    async def send_carbon_sense(self, date: str, sample: Dict[str, Measurement]):
        for room, measurement in sample.items():
            data = {"timestamp": date, "room_id": room, "co2": measurement.co2}

            await self._send_request(self._carbon_sense_url, data)

            logger.info(f"CarbonSense: {data} sent to {self._carbon_sense_url}")

    def is_allowed_room(self, room_id: str):
        return room_id in self.rooms

    def get_lux_meter_data(self, room_id: str):
        keys = list(self.data.keys())[-15:]
        measurements = [
            {"timestamp": key, "light_level": self.data[key][room_id].light}
            for key in keys
        ]
        return {"room_id": room_id, "measurements": measurements}

    async def _loop(self):
        while True:
            date = datetime.now().replace(second=0, microsecond=0).isoformat()

            if date not in self.data:
                await self._choose_sample(date)

            if len(self.data) > 15:
                self._cleanup()

            await asyncio.sleep(10)

    async def _choose_sample(self, date: str):
        self.change_room_cooldown -= 1

        if self.change_room_cooldown <= 0:
            current_hour = datetime.now().hour
            if current_hour > 23 or current_hour < 7:
                self.occupied_room = "bedroom"
            else:
                self.occupied_room = random.choice(self.rooms)

            self.change_room_cooldown = random.randint(5, 30)

        new_sample = {room: random.choice(self.negative_samples) for room in self.rooms}
        new_sample[self.occupied_room] = random.choice(self.positive_samples)
        self.data[date] = new_sample
        logger.info(
            f"Added new measurements for {date} / occupied room: {self.occupied_room} for {self.change_room_cooldown} minutes"
        )

        await self.save_smart_thermo(date, new_sample)
        await self.send_moisture_mate(date, new_sample)
        await self.send_carbon_sense(date, new_sample)

    async def _send_request(self, url: str, data: dict):
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=data)

        if r.status_code != httpx.codes.OK:
            logger.warning(f"Got status code: {r.status_code} for {url}")

    @staticmethod
    def _read_file(file_name: str):
        with open(Path(__file__).parent.parent / file_name) as f:
            data = [
                Measurement(**{k: float(v) for k, v in x.items()})
                for x in DictReader(f)
            ]
        return data

    def _cleanup(self):
        keys_to_remove = [
            key for key in self.data.keys() if key not in list(self.data.keys())[-15:]
        ]
        for key in keys_to_remove:
            del self.data[key]

        logger.info(f"Removed keys: {keys_to_remove}")
