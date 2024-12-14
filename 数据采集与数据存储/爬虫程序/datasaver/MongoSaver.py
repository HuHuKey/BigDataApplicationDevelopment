import warnings

import pymongo.errors
from pymongo import MongoClient
import pandas
from utils import ConnectionPool


def transToListOfLists(d: dict[str, list[str]]):
    return [{k: v for k, v in zip(d.keys(), values)} for values in zip(*d.values())]


# "mongodb://25.tcp.cpolar.top:12682/"
def saveDataFrameToMongoDB(df: pandas.DataFrame, db_name: str, collection: str,
                           host: str = ConnectionPool.str_):
    with MongoClient(host) as client:
        db = client[db_name]
        collection = db[collection]
        data_dict = df.to_dict("records")
        for upsert in data_dict:
            collection.update_one(upsert, {"$set": upsert}, upsert=True)


def saveDictToMongoDB(d: dict[str, list[str]], db_name: str, collection: str,
                      host: str = "mongodb://localhost:27017/"):
    with MongoClient(host) as client:
        db = client[db_name]
        collection = db[collection]
        tuples = [{k: v for k, v in zip(d.keys(), values)} for values in zip(*d.values())]
        for t in tuples:
            collection.update_one(t, {"$set": t}, upsert=True)
