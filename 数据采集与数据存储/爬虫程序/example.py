from crawler.Crawler import JDCrawler,TBCrawler
from datasaver.MongoSaver import saveDataFrameToMongoDB,saveDictToMongoDB
from datasaver.CSV import save_to_csv

if __name__ == "__main__":
    url1 = "http://www.jd.com"
    url2 = "http://www.taobao.com"
    keywords = input("请输入搜索关键词：")
    page = int(input("请输入爬取页数："))
    # crawler1= JDCrawler(name="JD", url=url1, cookie_filename='../conf/USER_COOKIES.txt')
    # crawler1.searchKeyWords(keywords=keywords)
    # dt1 = crawler1.getDictOfGoods(page)
    crawler2 = TBCrawler(name="TB", url=url2, cookie_filename='../conf/USER_COOKIES.txt')
    crawler2.searchKeyWords(keywords=keywords)
    dt2 = crawler2.getDictOfGoods(page)

    # print(dt1)
    print(dt2)
    # saveDictToMongoDB(dt1, 'jd', keywords[0])
    # saveDictToMongoDB(dt2, 'tb', keywords[:3])
    # save_to_csv(dt2,keywords[:3])
