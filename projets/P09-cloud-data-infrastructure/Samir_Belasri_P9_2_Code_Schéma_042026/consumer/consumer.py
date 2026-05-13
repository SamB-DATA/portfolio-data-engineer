import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


TOPIC = "client_tickets"
KAFKA_BROKER = "redpanda:9092"
OUTPUT_PATH = "/app/output/aggregated_tickets"
CHECKPOINT_PATH = "/app/output/checkpoints/aggregated_tickets"


def build_spark_session():
    spark = (
        SparkSession.builder
        .appName("TicketConsumer")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
        )
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")
    return spark


def get_ticket_schema():
    return StructType([
        StructField("ticket_id", IntegerType(), True),
        StructField("client_id", IntegerType(), True),
        StructField("created_at", StringType(), True),
        StructField("request", StringType(), True),
        StructField("request_type", StringType(), True),
        StructField("priority", StringType(), True),
    ])


def process_batch(batch_df, batch_id):
    print(f"Traitement du batch {batch_id}")

    if batch_df.count() == 0:
        print("Batch vide, rien à écrire.")
        return

    enriched_df = (
        batch_df
        .withColumn(
            "support_team",
            when(col("request_type") == "commercial", "Equipe Commerciale")
            .otherwise("Equipe Support Technique")
        )
    )

    aggregated_df = (
        enriched_df
        .groupBy("request_type", "priority", "support_team")
        .count()
    )

    aggregated_df.show(truncate=False)

    (
        aggregated_df
        .write
        .mode("append")
        .parquet(OUTPUT_PATH)
    )

    print(f"Résultats exportés dans : {OUTPUT_PATH}")


def main():
    os.makedirs("/app/output", exist_ok=True)

    spark = build_spark_session()
    schema = get_ticket_schema()

    kafka_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BROKER)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss", "false")
        .load()
    )

    parsed_df = (
        kafka_df
        .selectExpr("CAST(value AS STRING) as json_value")
        .select(from_json(col("json_value"), schema).alias("data"))
        .select("data.*")
    )

    query = (
        parsed_df.writeStream
        .foreachBatch(process_batch)
        .option("checkpointLocation", CHECKPOINT_PATH)
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()