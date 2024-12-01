from crawler.Crawler import JDCrawler, TBCrawler
from datasaver.MongoSaver import saveDataFrameToMongoDB, saveDictToMongoDB

if __name__ == "__main__":
    url1 = "http://www.jd.com"
    url2 = "http://www.taobao.com"
    keywords = ["西瓜"]
    page = 10
    crawler1 = JDCrawler(name="JD", cookie_filename='../conf/USER_COOKIES.txt')
    crawler1.searchKeyWords(keywords=keywords)
    dt1 = crawler1.getDataFrameOfGoods(page)
    # crawler2 = TBCrawler(name="TB", cookie_filename='../conf/USER_COOKIES.txt')
    # crawler2.searchKeyWords(keywords=keywords)
    # dt2 = crawler2.getDictOfGoods(page)

    # print(dt1)
    # print(dt2)
    saveDataFrameToMongoDB(dt1, 'jd', 'goods')
    # saveDictToMongoDB(dt2, 'tb', keywords[:3])
    # save_to_csv(dt2,keywords[:3])
