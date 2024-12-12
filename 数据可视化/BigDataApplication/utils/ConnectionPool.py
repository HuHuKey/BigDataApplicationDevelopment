from pymongo import MongoClient

host = '25.tcp.cpolar.top'
port = 12682
min_pool_size = 2
max_pool_size = 10

Client_Pool = MongoClient(rf"mongodb://{host}:{port}/?minPoolSize={min_pool_size}&maxPoolSize={max_pool_size}")
