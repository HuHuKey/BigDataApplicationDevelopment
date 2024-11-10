from crawler.Crawler import CookieCrawler

if __name__ == "__main__":
    url = "http://www.jd.com"
    keywords = ['沙子']
    crawler = CookieCrawler('../conf/USER_COOKIES.txt', url=url)
    crawler.searchKeyWords(keywords=['沙子'])
    df = crawler.getDataFrameOfGoods(30)
    df.to_csv('../data/goods.csv', encoding='utf-8')
