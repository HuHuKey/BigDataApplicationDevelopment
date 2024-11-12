from pymongo import MongoClient
import pandas


def transToListOfLists(d: dict[str, list[str]]):
    return [{k: v for k, v in zip(d.keys(), values)} for values in zip(*d.values())]


def saveDataFrameToMongoDB(df: pandas.DataFrame, db_name: str, collection: str,
                           host: str = "mongodb://localhost:27017/"):
    client = MongoClient(host)
    db = client[db_name]
    collection = db[collection]
    data_dict = df.to_dict("records")
    for upsert in data_dict:
        collection.update_one(upsert, {"$set": upsert}, upsert=True)


def saveDictToMongoDB(d: dict[str, list[str]], db_name: str, collection: str,
                      host: str = "mongodb://localhost:27017/"):
    client = MongoClient(host)
    db = client[db_name]
    collection = db[collection]
    tuples = [{k: v for k, v in zip(d.keys(), values)} for values in zip(*d.values())]
    for t in tuples:
        collection.update_one(t, {"$set": t}, upsert=True)
