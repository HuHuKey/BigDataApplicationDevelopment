from crawler.Crawler import JDCrawler
from datasaver.MongoSaver import saveDataFrameToMongoDB,saveDictToMongoDB

if __name__ == "__main__":
    url = "http://www.jd.com"
    keywords = ['沙子']
    crawler = JDCrawler(name="JD", url=url, cookie_filename='../conf/USER_COOKIES.txt')
    crawler.searchKeyWords(keywords=['沙子'])
    dt = crawler.getDictOfGoods(1)
    saveDictToMongoDB(dt, 'jd', 'goods')
