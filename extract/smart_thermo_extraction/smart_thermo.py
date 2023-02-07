import boto3
import time
import os
from kafka import KafkaProducer
import json
import logging

logger = logging.getLogger()

minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
minio_secret_key = os.environ.get("MINIO_SECRET_KEY")
KAFKA_BROKER_URL = os.environ.get("KAFKA_BOOTSTRAP_SERVER")

Producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            value_serializer=lambda x: json.dumps(x).encode('utf8'),
            api_version=(0, 10, 1)
        )


def smartthermo_data():
    # Connect to Minio using the S3 protocol
    s3 = boto3.resource("s3",
                        endpoint_url="http://minio:9000",
                        aws_access_key_id=minio_access_key,
                        aws_secret_access_key=minio_secret_key)
    while(True):
        time.sleep(60)
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
            logger.info(f"Smart_Thermo: {content}")
            record=Producer.send('smartthermo', value=content)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    smartthermo_data()