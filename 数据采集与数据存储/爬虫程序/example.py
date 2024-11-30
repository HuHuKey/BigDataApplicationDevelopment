import pandas as pd
import json
from crawler.Crawler import JDCrawler,TBCrawler
from datasaver.MongoSaver import saveDataFrameToMongoDB,saveDictToMongoDB

if __name__ == "__main__":
    url1 = "http://www.jd.com"
    url2 = "http://www.taobao.com"
    keywords = input("请输入搜索关键词：")
    page = int(input("请输入爬取页数："))
    # crawler1= JDCrawler(name="JD", url=url1, cookie_filename='../conf/USER_COOKIES.txt')
    # crawler1.searchKeyWords(keywords=keywords)
    # dt1 = crawler1.getDictOfGoods(page)
    # df1 = pd.DataFrame(dt1)
    # df1.to_csv('./data/jd/' + keywords[:3] + '.csv', encoding='utf-8')
    # saveDictToMongoDB(dt1, 'jd', keywords[::])
    # print("京东：", df1)

    crawler2 = TBCrawler(name="TB", url=url2, cookie_filename='../conf/USER_COOKIES.txt')
    crawler2.searchKeyWords(keywords=keywords)
    dt2 = crawler2.getDictOfGoods(page)
    df2 = pd.DataFrame(dt2)
    df2.to_csv('./data/tb/'+keywords[:3]+'.csv',encoding='utf-8')
    saveDictToMongoDB(dt2, 'tb', keywords[::])
    print("淘宝：", df2)
