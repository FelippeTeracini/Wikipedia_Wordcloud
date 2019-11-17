from pprint import pprint
from pyspark.sql import SparkSession
from os import environ

spark = SparkSession.builder.getOrCreate()

spark.read.format('xml').options(rowTag='page').load('s3://brubs-c/data/teste.xml') \
    .select('revision.text._VALUE') \
    .write \
    .option("header", "true") \
    .parquet("s3://brubs-c/data/teste_parquet")
