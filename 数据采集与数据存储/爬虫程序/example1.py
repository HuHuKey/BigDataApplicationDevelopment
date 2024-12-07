import threading
from crawler.Crawler import JDCrawler, TBCrawler
from datasaver.MongoSaver import saveDataFrameToMongoDB
import pandas as pd


def crawl_jd(keyword, page):
    url1 = "http://www.jd.com"
    crawler1 = JDCrawler(name="JD", cookie_filename='../conf/http_www.jd.com_USER_COOKIES.txt', url=url1)
    crawler1.searchKeyWords(keywords=[keyword])
    dt1 = crawler1.getDataFrameOfGoods(page)
    dt1['keywords'] = keyword
    saveDataFrameToMongoDB(dt1, 'E_Business_data', 'www.jd.com')
    csv_file = f'./data/jd/{keyword}.csv'
    dt1.to_csv(csv_file, encoding='utf-8')
    print(f'京东：{dt1}')


def crawl_tb(keyword, page):
    url2 = "http://www.taobao.com"
    crawler2 = TBCrawler(name="TB", cookie_filename='../conf/http_www.taobao.com_USER_COOKIES.txt', url=url2)
    crawler2.searchKeyWords(keywords=[keyword])
    page=1
    dt2 = crawler2.getDataFrameOfGoods(page)
    dt2['keywords'] = keyword
    saveDataFrameToMongoDB(dt2, 'E_Business_data', 'www.taobao.com')
    csv_file = f'./data/tb/{keyword}.csv'
    dt2.to_csv(csv_file, encoding='utf-8')
    print(f'淘宝：{dt2}')


if __name__ == "__main__":
    keywords = input("请输入搜索关键词（多个关键词用逗号分开）：").split('，')
    page = int(input("请输入页数："))
    threads = []
    for keyword in keywords:
        print(keyword)
        # 为京东创建线程
        jd_thread = threading.Thread(target=crawl_jd, args=(keyword,page))
        threads.append(jd_thread)
        # 为淘宝创建线程
        # tb_thread = threading.Thread(target=crawl_tb, args=(keyword,page))
        # threads.append(tb_thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("所有关键词的爬取任务已完成。")