import warnings

from pymongo.errors import ServerSelectionTimeoutError as Timeout
from utils import ConnectionPool
from crawler.Crawler import JDCrawler, TBCrawler
from datasaver.MongoSaver import saveDataFrameToMongoDB, saveDictToMongoDB

if __name__ == "__main__":
    url1 = "http://www.jd.com"
    url2 = "http://www.taobao.com"
    keywords = ["李宁"]
    page = 1
    crawler1 = JDCrawler(name="JD")
    crawler1.searchKeyWords(keywords=keywords)
    dt1 = crawler1.getDataFrameOfGoods(page)
    # crawler2 = TBCrawler(name="TB", cookie_filename='../conf/USER_COOKIES.txt')
    # crawler2.searchKeyWords(keywords=keywords)
    # dt2 = crawler2.getDictOfGoods(page)

    # print(dt1)
    # print(dt2)

    try:
        saveDataFrameToMongoDB(dt1, 'jd', 'goods', host=ConnectionPool.str_)
    except Timeout as e:
        warnings.warn("远程主机不可用，尝试使用本地连接")
        saveDataFrameToMongoDB(dt1, 'jd', 'goods', host="mongodb://localhost:27017")

    # saveDictToMongoDB(dt2, 'tb', keywords[:3])
    # save_to_csv(dt2,keywords[:3])
