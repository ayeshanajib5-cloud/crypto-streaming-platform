import os
from dotenv import load_dotenv

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType


load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto-prices")

POSTGRES_DB = os.getenv("POSTGRES_DB", "crypto_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "crypto_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "crypto_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

POSTGRES_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("currency", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("event_time", StringType(), True),
    StructField("source", StringType(), True),
])


def write_to_postgres(batch_df, batch_id):
    if batch_df.count() == 0:
        return

    output_df = batch_df.select(
    col("symbol"),
    col("currency"),
    col("price"),
    to_timestamp(col("event_time")).alias("event_time"),
    col("source"),
    current_timestamp().alias("processed_at")
    )

    output_df.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "crypto_prices") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

    print(f"Batch {batch_id} written to PostgreSQL")


def main():
    spark = SparkSession.builder \
        .appName("CryptoSparkStreaming") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()

    parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") \
        .filter(col("price").isNotNull())

    query = parsed_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()