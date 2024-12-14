from pymongo import MongoClient
from utils.ConnectionPool import Client_Pool


def read_jd_goods(db: MongoClient, collection: str = 'jdnew'):
    return db['E_Business_data'][collection].find({})


def read_taobao_goods(db: MongoClient, collection: str = 'tbnew'):
    return db['E_Business_data'][collection].find({})


if __name__ == '__main__':
    print(read_jd_goods(Client_Pool))
    print()
