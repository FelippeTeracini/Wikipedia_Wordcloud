from pprint import pprint
from pyspark.sql import SparkSession
from math import log10
import os
import pickle
import re

spark = SparkSession.builder.getOrCreate()

rdd = spark.read.format('parquet').load('s3://brubs-c/data/teste_parquet').rdd.map(tuple)

def cut_words(text):
    text_ready = str(text[0])
    return re.findall("\w+",text_ready) 

n_docs = rdd.count()

res = rdd.map(cut_words) \
    .flatMap(lambda x: [(k, 1) for k in set(x)]) \
    .reduceByKey(lambda x, y: x + y) \
    .filter(lambda x: x[1] > 20) \
    .map(lambda x: (x[0], log10(n_docs/x[1]))) \
    .collect()

with open ('idf.pickle', 'wb') as f:
    pickle.dump(res, f)

command = 'aws s3 cp idf.pickle s3://brubs-c/data/'
os.system(command)

