from pymongo import MongoClient
import pandas


def saveDataFrameToMongoDB(df: pandas.DataFrame, db_name: str, collection: str,
                           host: str = "mongodb://localhost:27017/"):
    client = MongoClient(host)
    db = client[db_name]
    collection = db[collection]
    data_dict = df.to_dict("records")
    collection.insert_many(data_dict)
