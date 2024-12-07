from pymongo import MongoClient

host = 'localhost'
port = 27017
min_pool_size = 2
max_pool_size = 10

Client_Pool = MongoClient(rf"mongodb://{host}:{port}/?minPoolSize={min_pool_size}&maxPoolSize={max_pool_size}")
