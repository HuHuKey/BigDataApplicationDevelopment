from pymongo import MongoClient

# # 远程连接
# host = '25.tcp.cpolar.top'
# port = 12682
# 本地连接
host = 'localhost'
port = 27017
min_pool_size = 2
max_pool_size = 10
str_ = f'mongodb://{host}:{port}/'

redis_host = r'127.0.0.1'
redis_port = 6379
redis_url = rf"redis://{redis_host}:{redis_port}"

url = rf"mongodb://{host}:{port}"
Client_Pool = MongoClient(rf"mongodb://{host}:{port}/?minPoolSize={min_pool_size}&maxPoolSize={max_pool_size}")
