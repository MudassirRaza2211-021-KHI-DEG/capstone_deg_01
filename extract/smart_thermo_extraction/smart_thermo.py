import json
import logging
import os
import time

import boto3
from kafka import KafkaProducer

logger = logging.getLogger()

MINIO_ENDPOINT_URL = os.environ.get("MINIO_ENDPOINT_URL")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")

producer = None


def get_smartthermo_data_periodically():
    while True:
        time.sleep(60)
        get_smart_thermo_data()


def get_smart_thermo_data():
    # Connect to Minio using the S3 protocol
    s3 = boto3.resource(
        "s3",
        endpoint_url=MINIO_ENDPOINT_URL,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    # List all objects in the bucket
    bucket = s3.Bucket("capstondeg01")
    objects = list(bucket.objects.all())
    # Read the contents of the last object if it's a csv file
    obj = list(filter(lambda o: o.key.endswith(".csv"), objects))[-1]
    obj = s3.Object("capstondeg01", obj.key)
    content = obj.get()["Body"].read().decode("utf-8")
    logger.info(f"Read SmartThermo data from MinIO: {content}")
    record = producer.send("smartthermo", value=content)
    logger.debug(
        f"Smart-Thermo data sent to Kafka topic successfully: {record}")

    lines = content.strip().split("\n")
    header = lines[0].strip().split(",")
    room_index = header.index("room_id")

    for line in lines[1:]:
        values = line.strip().split(",")
        room_id = values[room_index]

        data = dict(zip(header, values))
        json_data = json.dumps(data)
        json_data = json.loads(json_data)
        json_data['temperature'] = float(json_data['temperature'])

        record = producer.send('smartthermo', key=(
            room_id).encode('utf-8'), value=json_data)


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode("utf8"),
        api_version=(0, 10, 1),
    )
    logging.basicConfig(level=logging.DEBUG)
    get_smartthermo_data_periodically()
