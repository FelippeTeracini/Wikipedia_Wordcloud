
from pprint import pprint
from pyspark.sql import SparkSession
from math import log10
import pickle
from collections import defaultdict
import os
import re

command = 'aws s3 cp s3://brubs-c/data/idf.pickle main_idf.pickle'
os.system(command)

with open('main_idf.pickle', 'rb') as f:
    idf = pickle.load(f)

spark = SparkSession.builder.getOrCreate()

sc = spark.sparkContext

broadcast_var = sc.broadcast(idf)

def acha_palavras_top(texto):
    if texto is not None:
        idf = broadcast_var.value
        idf = dict(idf)
        text_ready = str(texto)
        palavras = re.findall("\w+", text_ready)
        tf = defaultdict(int)
        for p in palavras:
            tf[p] += 1
        for p in tf:
            if p in idf:
                tf[p] *= idf[p]
            else:
                tf[p] *= 0
        tfidf = [(v, p) for p, v in tf.items()]
        tfidf = sorted(tfidf, reverse=True)
        return [x[1] for x in tfidf[:25]]
    else:
        lista = []
        return lista

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

rdd = spark.read.format('parquet').load('s3://brubs-c/data/main_parquet').rdd.map(tuple)

res = rdd \
    .map(lambda x: x[0])\
    .map(acha_palavras_top) \
    .flatMap(gera_pares) \
    .groupByKey() \
    .map(conta_palavras) \
    .collect()

print(res)

with open('final.pickle', 'wb') as f:
    pickle.dump(res, f)

command = 'aws s3 cp final.pickle s3://brubs-c/data/'
os.system(command)
