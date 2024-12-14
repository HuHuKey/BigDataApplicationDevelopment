import warnings

import pymongo.errors
from pymongo import MongoClient
import pandas


def transToListOfLists(d: dict[str, list[str]]):
    return [{k: v for k, v in zip(d.keys(), values)} for values in zip(*d.values())]


def saveDataFrameToMongoDB(df: pandas.DataFrame, db_name: str, collection: str,
                           host: str = "mongodb://25.tcp.cpolar.top:11723"):
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


def upsertTuple(client: MongoClient, db_name: str, collection: str, keys: list[str], t: dict[str, str]):
    db = client[db_name]
    collection = db[collection]
    keymap = {keys[i]: t[keys[i]] for i in range(len(keys))}
    collection.update_one(keymap, {"$set": t}, upsert=True)
