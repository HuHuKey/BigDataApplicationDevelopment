import datetime
import decimal

import pymongo
from decimal import Decimal
from utils.ConnectionPool import Client_Pool


def clear_jd():
    # 连接到MongoDB服务器
    client = Client_Pool

    # 获取数据库对象
    db = client["E_Business_data"]

    # 获取原始集合对象
    db_collection = db["jd"]

    # 创建新集合jdnew（如果不存在会自动创建）
    new_collection = db["jdnew"]

    # 查询集合中的所有文档
    documents = db_collection.find()

    # 定义计数器i，初始值为1
    i = 1
    skipped_count = 0  # 跳过文档计数器
    updated_count = 0  # 更新成功的文档计数

    # 存储要插入的文档
    bulk_operations = []

    for document in documents:
        name_value = document.get("name")
        if name_value and isinstance(name_value, str):
            document["name"] = name_value.replace("\n", "")

        # 处理price字段
        price_value = document.get("price")
        if price_value:
            # 新增：检查price_value类型是否符合预期，如果不符合直接记录错误并跳过该文档
            if not isinstance(price_value, (str, float, int)):
                print(f"跳过文档: {document.get('name')} - price字段类型不符合预期")
                skipped_count += 1
                continue
            try:
                # 先尝试将price_value转换为字符串（如果本身不是字符串的话），再构造Decimal对象
                decimal_price = Decimal(str(price_value))
                document["price"] = round(float(decimal_price), 2)
            except decimal.InvalidOperation as e:
                print(f"跳过文档: {document.get('name')} - price字段转换失败，原因: {e}")
                skipped_count += 1
                continue

        # 处理commentCount字段
        comment_count_value = document.get("commentCount")
        if comment_count_value and isinstance(comment_count_value, str):
            comment_count_value = comment_count_value.replace("+", "")
            comment_count_value = comment_count_value.replace("万", "0000")
            try:
                document["commentCount"] = int(comment_count_value)
            except ValueError:
                print(f"跳过文档: {document.get('name')} - commentCount字段转换失败")
                skipped_count += 1
                continue

        # 计算gross sales字段
        price = document.get("price", 0)
        comment_count = document.get("commentCount", 0)
        try:
            decimal_price = Decimal(str(price))
            decimal_comment_count = Decimal(str(comment_count))
            document["gross sales"] = round(float(decimal_price * decimal_comment_count), 2)
        except decimal.InvalidOperation as e:
            print(f"跳过文档: {document.get('price')} - gross sales字段计算失败，原因: {e}")
            skipped_count += 1
            continue

        crawl_time = document.get("crawlTime", datetime.datetime.now())
        if isinstance(crawl_time, datetime.datetime):
            crawl_time = crawl_time.strftime("%Y-%m-%d")
        document["crawlTime"] = crawl_time

        # 添加到批量操作列表中，无需删除 _id 字段
        bulk_operations.append(
            pymongo.UpdateOne(
                {"_id": document["_id"]},  # 使用 _id 作为查找条件
                {"$set": document},
                upsert=True
            )
        )

        i += 1

        if len(bulk_operations) >= 100:
            result = new_collection.bulk_write(bulk_operations)
            updated_count += result.modified_count + result.upserted_count
            bulk_operations = []

    if bulk_operations:
        result = new_collection.bulk_write(bulk_operations)
        updated_count += result.modified_count + result.upserted_count

    # 输出i的值和被跳过的文档总数
    print(f"读取的文档总数: {i - 1}")  # 输出时减去1以获得真正的文档数
    print(f"跳过的文档总数: {skipped_count}")
    print(f"成功更新或插入的文档总数: {updated_count}")


def clear_tb():
    # 连接到MongoDB服务器
    client = Client_Pool

    # 获取数据库对象
    db = client["E_Business_data"]

    # 获取原始集合对象
    db_collection = db["www.taobao.com"]

    # 创建新集合 tbnew（如果不存在会自动创建）
    new_collection = db["tbnew"]

    # 查询集合中的所有文档
    documents = db_collection.find()

    # 存储要批量插入或更新的操作列表
    bulk_operations = []

    # 定义计数器来记录读取的文档数
    document_count = 0

    # 修改文档并准备批量插入
    for document in documents:
        document_count += 1  # 每读取一条文档，计数器加1

        # 删除 href 字段
        if "href" in document:
            document.pop("href")  # 使用 pop 方法删除 href 字段

        # 处理 city 字段
        city_value = document.get("city", "")
        if " " in city_value:
            province, city = city_value.split(" ", 1)
        else:
            province = city_value
            city = city_value

        document["province"] = province
        document["city"] = city

        # 处理 price 字段
        price_value = document.get("price")
        if price_value is not None:
            try:
                document["price"] = round(float(price_value), 2)
            except (ValueError, TypeError):
                continue  # 如果无法转换则跳过该文档

        # 处理 commentCount 字段
        comment_count_value = document.get("commentCount", "")
        if isinstance(comment_count_value, str):
            # 去掉“人付款”、“+”号，并将“万”替换为“0000”
            comment_count_value = comment_count_value.replace("人付款", "").replace("+", "").replace("万",
                                                                                                     "0000").strip()
            try:
                document["commentCount"] = int(comment_count_value)
            except ValueError:
                continue  # 如果无法转换则跳过该文档

        # 计算 gross sales 字段
        price = document.get("price", 0)  # 默认值为0
        comment_count = document.get("commentCount", 0)  # 默认值为0
        document["gross sales"] = round(price * comment_count, 2)  # 计算总销售额并保留两位小数

        # 添加到批量操作列表中
        bulk_operations.append(
            pymongo.UpdateOne(
                {"_id": document["_id"]},  # 使用 _id 作为查找条件
                {"$set": document},  # 更新文档
                upsert=True  # 如果该文档不存在，则插入新文档
            )
        )

        # 每100条操作执行一次批量写入
        if len(bulk_operations) >= 100:
            new_collection.bulk_write(bulk_operations)
            bulk_operations = []  # 清空操作列表

    # 插入剩余的操作
    if bulk_operations:
        new_collection.bulk_write(bulk_operations)

    # 输出读取的文档总数
    print(f"总共读取了 {document_count} 个文档。")
    print("所有修改后的文档已保存到 tbnew 集合中。")


def jd_tuple_clear(document: dict):
    name_value = document.get("name")
    if name_value and isinstance(name_value, str):
        document["name"] = name_value.replace("\n", "")

    # 处理price字段
    price_value = document.get("price")
    if price_value:
        # 新增：检查price_value类型是否符合预期，如果不符合直接记录错误并跳过该文档
        if not isinstance(price_value, (str, float, int)):
            print(f"跳过文档: {document.get('name')} - price字段类型不符合预期")
        try:
            # 先尝试将price_value转换为字符串（如果本身不是字符串的话），再构造Decimal对象
            decimal_price = Decimal(str(price_value))
            document["price"] = round(float(decimal_price), 2)
        except decimal.InvalidOperation as e:
            print(f"跳过文档: {document.get('name')} - price字段转换失败，原因: {e}")
            return False
    # 处理commentCount字段
    comment_count_value = document.get("commentCount")
    if comment_count_value and isinstance(comment_count_value, str):
        comment_count_value = comment_count_value.replace("+", "")
        comment_count_value = comment_count_value.replace("万", "0000")
        try:
            document["commentCount"] = int(comment_count_value)
        except ValueError:
            print(f"跳过文档: {document.get('name')} - commentCount字段转换失败")
            return False

    # 计算gross sales字段
    price = document.get("price", 0)
    comment_count = document.get("commentCount", 0)
    try:
        decimal_price = Decimal(str(price))
        decimal_comment_count = Decimal(str(comment_count))
        document["gross sales"] = round(float(decimal_price * decimal_comment_count), 2)
    except decimal.InvalidOperation as e:
        print(f"跳过文档: {document.get('price')} - gross sales字段计算失败，原因: {e}")
        return False

    crawl_time = document.get("crawlTime", datetime.datetime.now())
    if isinstance(crawl_time, datetime.datetime):
        crawl_time = crawl_time.strftime("%Y-%m-%d")
    document["crawlTime"] = crawl_time
    return True


if __name__ == '__main__':
    clear_tb()
    clear_jd()
