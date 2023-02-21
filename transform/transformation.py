import os
from typing import List, Tuple

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame, SparkSession

postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")
postgres_table = os.environ.get("POSTGRES_TABLE")
postgres_url = os.environ.get("POSTGRES_URL")


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("Tutorial App")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1")
        .config("spark.jars", "/usr/local/lib/python3.10/site-packages/pyspark/jars/postgresql-42.3.1.jar")
        .getOrCreate()
    )
    return spark


def Show_SparkUI_details() -> None:
    spark = create_spark_session()
    print(spark)


def create_schema(columns: List[Tuple[str, str]]) -> T.StructType:
    schema = T.StructType()
    for col_name, col_type in columns:
        if col_type == "string":
            schema = schema.add(col_name, T.StringType())
        elif col_type == "float":
            schema = schema.add(col_name, T.FloatType())
    return schema


def read_data_from_kafka_topic(spark: SparkSession, Topic_name: str) -> DataFrame:
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", Topic_name) \
        .option("startingOffsets", "latest") \
        .option("maxOffsetsPerTrigger", 4) \
        .load()
    return df


def transform_sensor_data(df: DataFrame, schema: T.StructType) -> DataFrame:
    df = df.withColumn("message_content", F.from_json(
        F.col("value").cast("string"), schema))
    df_minimal = df.select("message_content.*")
    return df_minimal


def merge_dataframes(dfs: List[DataFrame], on: List[str], how: str) -> DataFrame:
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = merged_df.join(df, on=on, how=how)
    return merged_df


if __name__ == '__main__':
    spark = create_spark_session()
    Show_SparkUI_details()
    moisturemate_columns = [("timestamp", "string"),
                            ("room_id", "string"),
                            ("humidity", "float"),
                            ("humidity_ratio", "float")]
    carbonsense_columns = [("timestamp", "string"),
                           ("room_id", "string"),
                           ("co2", "float")]
    luxmeter_columns = [("timestamp", "string"),
                        ("light_level", "float"),
                        ("room_id", "string")]
    smartthermo_columns = [("timestamp", "string"),
                           ("room_id", "string"),
                           ("temperature", "float")]
    moisturemate_schema = create_schema(moisturemate_columns)
    carbonsense_schema = create_schema(carbonsense_columns)
    luxmeter_schema = create_schema(luxmeter_columns)
    smartthermo_schema = create_schema(smartthermo_columns)
    df_moisturemate = read_data_from_kafka_topic(spark, "moisturemate")
    df_carbonsense = read_data_from_kafka_topic(spark, "carbonsense")
    df_luxmeter = read_data_from_kafka_topic(spark, "luxmeter")
    df_smartthermo = read_data_from_kafka_topic(spark, "smartthermo")
    df_minimal_moisturemate = transform_sensor_data(
        df_moisturemate, moisturemate_schema)
    df_minimal_carbonsense = transform_sensor_data(
        df_carbonsense, carbonsense_schema)
    df_minimal_luxmeter = transform_sensor_data(df_luxmeter, luxmeter_schema)
    df_minimal_smartthermo = transform_sensor_data(
        df_smartthermo, smartthermo_schema)
    merged_df = merge_dataframes(dfs=[df_minimal_moisturemate, df_minimal_carbonsense,
                                 df_minimal_luxmeter, df_minimal_smartthermo], on=["timestamp", "room_id"], how="inner")
    # Converting 'timestamp: string' to 'timestamp: timestamp', so that we can sort time
    merged_df = merged_df.withColumn("timestamp", F.to_timestamp(
        merged_df["timestamp"], "yyyy-MM-dd'T'HH:mm:ss"))
    query = (
        merged_df.writeStream
        .outputMode("append")
        .option("truncate", False)
        .foreachBatch(lambda batchDF, batchId: batchDF.write.jdbc(
            url=postgres_url,
            table=postgres_table,
            mode="append",
            properties={"user": postgres_user, "password": postgres_password}
        ))
        .start()
    )
    query.awaitTermination()
