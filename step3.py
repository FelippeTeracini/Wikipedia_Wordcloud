from pprint import pprint
from pyspark.sql import SparkSession
from math import log10
import pickle
from collections import defaultdict
import os
import re

command = 'aws s3 cp s3://brubs-c/data/idf.pickle idf.pickle'
os.system(command)

with open('idf.pickle', 'rb') as f:
    idf = pickle.load(f)

spark = SparkSession.builder.getOrCreate()

sc = spark.sparkContext

broadcast_var = sc.broadcast(idf)

def acha_palavras_top(texto):
    idf = broadcast_var.value
    idf = dict(idf)
    palavras = re.findall("\w+", texto)
    tf = defaultdict(int)
    for p in palavras:
        tf[p] += 1
    for p in tf:
        tf[p] *= idf[p]
    tfidf = [(v, p) for p, v in tf.items()]
    tfidf = sorted(tfidf, reverse=True)
    return [x[1] for x in tfidf[:25]]

def gera_pares(lista_palavras):
    pares = []
    for p in lista_palavras:
        for q in lista_palavras:
            if p != q:
                pares.append((p,q))
    return pares

def conta_palavras(item):
    contagem = defaultdict(int)
    for p in item[1]:
        contagem[p] += 1
    return (item[0], contagem)

rdd = spark.read.format('parquet').load('s3://brubs-c/data/teste_parquet').rdd.map(tuple)

res = rdd \
    .map(lambda x: x[0])\
    .map(acha_palavras_top) \
    .flatMap(gera_pares) \
    .groupByKey() \
    .map(conta_palavras) \
    .collect()

print(res)

with open('teste_final.pickle', 'wb') as f:
    pickle.dump(res, f)

command = 'aws s3 cp teste_final.pickle s3://brubs-c/data/'
os.system(command)
