from crawler.Crawler import JDCrawler, TBCrawler
from datasaver.MongoSaver import saveDataFrameToMongoDB

if __name__ == "__main__":
    url1 = "http://www.jd.com"
    url2 = "http://www.taobao.com"
    keywords = input("请输入搜索关键词：")
    # page = int(input("请输入爬取页数："))
    page = 2
    #京东
    crawler1 = JDCrawler(name="JD", cookie_filename='../conf/http_www.jd.com_USER_COOKIES.txt', url=url1)
    crawler1.searchKeyWords(keywords=keywords)
    dt1 = crawler1.getDataFrameOfGoods(page)
    dt1['keywords'] = keywords
    saveDataFrameToMongoDB(dt1, 'E_Business_data','www.jd.com')
    csv_file = f'./data/jd/{keywords}.csv'
    dt1.to_csv(csv_file, encoding='utf-8')
    print(f'京东：{dt1}')


    #淘宝
    crawler2 = TBCrawler(name="TB", cookie_filename='../conf/http_www.taobao.com_USER_COOKIES.txt', url=url2)
    crawler2.searchKeyWords(keywords=keywords)
    dt2 = crawler2.getDataFrameOfGoods(page)
    dt2['keywords'] = keywords
    saveDataFrameToMongoDB(dt2, 'E_Business_data', 'www.taobao.com')
    csv_file = f'./data/tb/{keywords}.csv'
    dt2.to_csv(csv_file, encoding='utf-8')
    print(f'淘宝：{dt2}')

