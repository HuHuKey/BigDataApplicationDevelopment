import mongoengine
from EBAsite.settings import DATABASES
from utils.ConnectionPool import host, port

mongoengine.connect(DATABASES['mongodb']['NAME'], host=host, port=port)


# Create your models here.
class SalesData(mongoengine.Document):
    crawl_time = mongoengine.DateTimeField(db_field="crawlTime")
    product_name = mongoengine.StringField()
    product_price = mongoengine.FloatField(db_field="price")
    comment_count = mongoengine.IntField(db_field="commentCount")


class Jdnew(mongoengine.Document):
    crawl_time = mongoengine.DateTimeField(db_field="crawlTime")
    name = mongoengine.StringField()
    price = mongoengine.FloatField(db_field="price")
    commentCnt = mongoengine.IntField(db_field="commentCount")
    grossSales = mongoengine.IntField(db_field="gross sales")
    province = mongoengine.StringField()
    href = mongoengine.StringField()
    supplier = mongoengine.StringField()
    keywords = mongoengine.StringField()

    def __dict__(self):
        return {
            "crawl_time": self.crawl_time,
            "name": self.name,
            "price": self.price,
            "commentCnt": self.commentCnt,
            "grossSales": self.grossSales,
            "province": self.province,
            "href": self.href,
            "supplier": self.supplier,
            "keywords": self.keywords
        }


class Jd(mongoengine.Document):
    crawl_time = mongoengine.DateTimeField(db_field="crawlTime")
    name = mongoengine.StringField()
    price = mongoengine.FloatField(db_field="price")
    commentCnt = mongoengine.IntField(db_field="commentCount")
    grossSales = mongoengine.IntField(db_field="gross sales")
    href = mongoengine.StringField()
    supplier = mongoengine.StringField()
    keywords = mongoengine.StringField()


class Tbnew(mongoengine.Document):
    crawl_time = mongoengine.DateTimeField(db_field="crawlTime")
    name = mongoengine.StringField()
    price = mongoengine.FloatField(db_field="price")
    commentCnt = mongoengine.IntField(db_field="commentCount")
    grossSales = mongoengine.IntField(db_field="gross sales")
    province = mongoengine.StringField()
    supplier = mongoengine.StringField()
    keywords = mongoengine.StringField()
