import boto3
import time
import os
from kafka import KafkaProducer
import json
import logging

logger = logging.getLogger()

MINIO_ENDPOINT_URL = os.environ.get("MINIO_ENDPOINT_URL")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")

producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('utf8'),
            api_version=(0, 10, 1)
        )


def get_smartthermo_data_periodically():
    while(True):
        time.sleep(60)
        get_smart_thermo_data()


def get_smart_thermo_data():
    # Connect to Minio using the S3 protocol
    s3 = boto3.resource("s3",
                        endpoint_url=f"{MINIO_ENDPOINT_URL}",
                        aws_access_key_id=MINIO_ACCESS_KEY ,
                        aws_secret_access_key=MINIO_SECRET_KEY )
     
    # List all objects in the bucket
    bucket = s3.Bucket("capstondeg01")
    # filter method will return a list of all those csv files in the folder.
    objects = list(bucket.objects.filter())
    # Get last object
    obj = objects[-1]
    # Read the contents of the object if it's a csv file
    if obj.key.endswith(".csv"):
        obj = s3.Object("capstondeg01", obj.key)
        content = obj.get()["Body"].read().decode("utf-8")
        logger.info(f"Read SmartThermo data from MinIO: {content}")
        record=producer.send('smartthermo', value=content)
        logger.debug(f"Smart-Thermo data sent to Kafka topic successfully: {record}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    get_smartthermo_data_periodically()
