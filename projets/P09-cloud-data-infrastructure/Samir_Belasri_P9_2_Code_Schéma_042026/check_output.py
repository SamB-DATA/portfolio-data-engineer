from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum

BASE_DIR = Path("output/aggregated_tickets")

parquet_files = [str(p) for p in BASE_DIR.glob("*.snappy.parquet") if p.is_file()]

print("Fichiers parquet trouvés :")
for f in parquet_files:
    print("-", f)

print("Nombre de fichiers parquet :", len(parquet_files))

if not parquet_files:
    raise FileNotFoundError(
        "Aucun fichier .snappy.parquet trouvé dans output/aggregated_tickets"
    )

spark = (
    SparkSession.builder
    .appName("CheckOutput")
    .master("local[*]")
    .getOrCreate()
)

df = spark.read.parquet(*parquet_files)

print("Résultats intermédiaires lus depuis Parquet :")
df.show(100, truncate=False)

final_df = (
    df.groupBy("request_type", "priority", "support_team")
      .agg(spark_sum("count").alias("total_tickets"))
      .orderBy("request_type", "priority", "support_team")
)

print("Résultats agrégés finaux :")
final_df.show(100, truncate=False)

spark.stop()