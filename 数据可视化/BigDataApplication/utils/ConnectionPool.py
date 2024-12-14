from pymongo import MongoClient

host = '127.0.0.1'
port = 27017
# host = '25.tcp.cpolar.top'
# port = 12682
min_pool_size = 2
max_pool_size = 10

redis_host = r'127.0.0.1'
redis_port = 6379
redis_url = rf"redis://{redis_host}:{redis_port}"

url = rf"mongodb://{host}:{port}"
Client_Pool = MongoClient(rf"mongodb://{host}:{port}/?minPoolSize={min_pool_size}&maxPoolSize={max_pool_size}")
