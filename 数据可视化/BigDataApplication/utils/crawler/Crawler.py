import random
import types
import warnings
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.crawler.cookies.CookieSaver import CookieSaver
from selenium.webdriver.edge.options import Options
from utils.crawler.CrawlerData import CrawlerData
from pyquery import PyQuery as pq


class Crawler(metaclass=ABCMeta):
    @abstractmethod
    def searchKeyWords(self, keywords):
        pass

    @abstractmethod
    def getOnePageOfGoods(self):
        pass

    @abstractmethod
    def scrollDown(self):
        pass

    @abstractmethod
    def turnToNextPage(self):
        """
        翻页
        :return: None
        """
        pass

    @abstractmethod
    def getDictOfGoods(self, page_num: int):
        pass

    @abstractmethod
    def getDataFrameOfGoods(self, page_num: int):
        pass


class BaseCrawler(Crawler):
    name = None
    url = None
    driver: webdriver = None
    col2css: dict[str, str]
    goods_css = None
    search_bar = None
    max_page_css = None
    next_page_css = None
    options: Options = None
    data: CrawlerData

    def __init__(self, name: str,
                 url: str,
                 search_bar="input[type='text']",
                 max_page_css='#J_bottomPage > span.p-skip > em:nth-child(1) > b',
                 goods_css: str = '#J_goodsList > ul > li',
                 next_page_css='KEY.RIGHT',
                 options: Options = None,
                 col2css: dict[str, str] = None,
                 ):
        self.keywords = None
        self.name = name
        self.url = url
        if options is None:
            options = Options()
        if col2css is None:
            col2css = {
                'name': 'div.p-name.p-name-type-2 > a > em',
                'price': 'div.p-price > strong > i',
                'supplier': 'div.p-shop > span > a'
            }
        self.col2css = col2css
        self.data = CrawlerData(col2css)
        self.options = options
        self.goods_css = goods_css
        self.search_bar = search_bar
        self.max_page_css = max_page_css
        self.next_page_css = next_page_css
        options.add_experimental_option('detach', False)  # 规避程序运行完自动退出浏览器
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0')
        self.driver = webdriver.Edge(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(url)

    def searchKeyWords(self, keywords: list):
        try:
            (WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.search_bar))))
        except Exception as e:
            warnings.warn(f"无法找到搜索框，请检查网络:{e}")
            return
        self.randomWait(0.8, 2)
        self.keywords = keywords
        text_input = self.driver.find_element(By.CSS_SELECTOR, self.search_bar)
        text_input.send_keys(" ".join(keywords))
        text_input.send_keys(webdriver.Keys.RETURN)

    def collectGoodsData(self, goods: str) -> None:
        # data_list = dict(zip(self.col2css.keys(), [[] for _ in self.col2css.keys()]))
        for good in goods:
            g = pq(good)
            self.appendGoodsList(g)
            self.data.nextTuple('jd')

    def appendGoodsList(self, g):
        for (k, v) in self.col2css.items():
            if v == '':
                continue
            elif isinstance(v, str):
                try:
                    element = g(v)
                    # data_list[k].append(element.text())
                    self.data.write(k, element.text())
                except Exception as e:
                    print(e)
            elif callable(v):
                self.data.write(k, v())
                # data_list[k].append(v())
            elif isinstance(v, types.FunctionType):
                if v.__code__.co_argcount == 0:
                    # data_list[k].append(v())
                    self.data.write(k, v())
                else:
                    self.data.write(k, v(g))
                    # data_list[k].append(v(g))

    def getOnePageOfGoods(self):
        """
        获取一页商品信息,用pquery解析html比直接用webdriver快

        :returns: 返回一个类似于
        {'name': ['name1', 'name2'],
        'price': ['price1', 'price2'],
        ...}
        的一个字典
        """
        html = self.driver.page_source
        doc = pq(html)
        goods = doc(self.goods_css).items()
        self.collectGoodsData(goods)

    @abstractmethod
    def turnToNextPage(self):
        """
        翻页，根据不同的网站需要实现重写不同的方法
        :return: None
        """
        pass
        body = self.driver.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(webdriver.Keys.RIGHT)
        self.scrollDown()

    def scrollDown(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def getDictOfGoods(self, page_num: int = 30) -> CrawlerData:
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.max_page_css)))
            total_page = self.driver.find_element(By.CSS_SELECTOR, self.max_page_css).text
        except Exception as e:
            warnings.warn(f"无法找到maxPageNum,使用默认参数total_page=100")
            total_page = 100
        total_page = int(total_page)
        # data_list = dict(zip(self.col2css.keys(), [[] for _ in self.col2css.keys()]))
        for _ in range(min(page_num, total_page)):
            self.getOnePageOfGoods()
            # for col in self.col2css.keys():
            #     data_list[col].extend(new_goods[col])
            self.turnToNextPage()
        return self.data

    def close(self):
        self.driver.close()

    def getDataFrameOfGoods(self, page_num: int = 30) -> pd.DataFrame:
        goods = self.getDictOfGoods(page_num)
        df = pd.DataFrame(goods)
        return df

    def randomWait(self, min_time: float = 0.5, max_time: float = 1.5):
        self.driver.implicitly_wait(random.uniform(min_time, max_time))


class CookieCrawler(BaseCrawler):
    data_list = {}

    @abstractmethod
    def turnToNextPage(self):
        pass

    cookie_saver: CookieSaver = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cookie_saver = CookieSaver(self.driver)

        not_load = not self.cookie_saver.load_cookies()
        invalid = not self.cookie_saver.is_cookie_valid()

        while not_load or invalid:
            # TODO: 这里可以改成一个Web交互式界面
            input("Cookie is failed to load, please press 'Enter' after login.")
            self.cookie_saver.refresh_cookies()
            self.cookie_saver.save_cookies()
            not_load = not self.cookie_saver.load_cookies()
            invalid = not self.cookie_saver.is_cookie_valid()

    def getDataFrameOfGoods(self, page_num: int = 30) -> pd.DataFrame:
        return super().getDataFrameOfGoods(page_num)

    def searchKeyWords(self, keywords: list):
        self.driver.get(self.url)
        super().searchKeyWords(keywords)


class HeadlessCrawler(CookieCrawler):
    @abstractmethod
    def turnToNextPage(self):
        pass

    def __init__(self, *args, **kwargs):
        options = Options()
        # 设置无头模式
        options.add_argument("--headless")
        # 设置禁用沙盒模式
        options.add_argument("--disable-dev-shm-usage")
        # 设置加载策略
        options.page_load_strategy = "eager"
        super().__init__(*args, options=options, **kwargs)


def getTodayDate():
    return datetime.now().date().isoformat()


class JDCrawler(HeadlessCrawler):
    def __init__(self, name: str):
        args = (name, 'http://www.jd.com')
        kwargs = {
            "col2css": {
                'crawlTime': getTodayDate,
                'name': 'div.p-name.p-name-type-2 > a > em',
                'price': 'div.p-price > strong > i',
                'supplier': 'div.p-shop > span > a',
                'commentCount': 'div.p-commit >strong >a',
                'href': ''
            },
            "goods_css": '#J_goodsList > ul > li',
            "search_bar": 'input[type="text"]',
            "max_page_css": '#J_bottomPage > span.p-skip > em:nth-child(1) > b',
            'next_page_css': 'KEY.RIGHT',
        }
        super().__init__(*args, **kwargs)

    def turnToNextPage(self):
        """
        京东翻页
        :return: None
        """
        if self.next_page_css == 'KEY.RIGHT':
            body = self.driver.find_element(By.CSS_SELECTOR, 'body')
            body.send_keys(webdriver.Keys.RIGHT)
            self.scrollDown()
            return
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.next_page_css)))
        except Exception as e:
            warnings.warn(f"无法找到下一页按钮:{e}")
            return

        self.driver.find_element(By.CSS_SELECTOR, self.next_page_css).click()
        self.scrollDown()

    def scrollDown(self):
        self.driver.refresh()
        pass

    def appendGoodsList(self, g):
        super().appendGoodsList(g)
        k = 'href'
        v = ("https:" + g('div.p-name.p-name-type-2 > a').attr['href'])
        self.data.write(k, v)
        k = 'keywords'
        v = self.keywords
        self.data.write(k, v)


class TBCrawler(CookieCrawler):
    def __init__(self, name: str):
        super().__init__(name, "www.taobao.com")
        self.col2css = {
            'crawlTime': getTodayDate,
            'name': "div[class *= 'title'] > span",  # 淘宝商品名称的选择器
            'price': "div[class*='priceWrapper']> div:nth-child(2)",  # 淘宝商品价格的选择器
            'supplier': "div[class*='shopTextWrapper']> span.shopNameText--DmtlsDKm",  # 淘宝供应商名称的选择器
            'city': 'div.procity--wlcT2xH9 > span',
            'commentCount': 'div.priceWrapper--dBtPZ2K1 > span.realSales--XZJiepmt',  # 淘宝评论数量的选择器
            'href': ''
        }
        self.goods_css = '#content_items_wrapper > div'  # 淘宝商品列表的选择器
        self.search_bar = 'input[name = "q"]'  # 淘宝搜索框的选择器
        self.max_page_css = '#search-content-leftWrap > div.leftContent--BdYLMbH8 > div.pgWrap--RTFKoWa6 > div > div > div > button:nth-child(7) > span'  # 淘宝总页数的选择器
        self.next_page_css = "div.pgWrap--RTFKoWa6 > div > div > button[class *= 'next-next']"  # 淘宝下一页的选择器

    def turnToNextPage(self):
        """
        淘宝翻页
        :return: None
        """
        self.randomWait()
        if self.next_page_css == 'KEY.RIGHT':
            body = self.driver.find_element(By.CSS_SELECTOR, 'body')
            body.send_keys(webdriver.Keys.RIGHT)
            self.scrollDown()
            return
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.next_page_css)))
        except Exception as e:
            warnings.warn(f"无法找到下一页按钮:{e}")
            return
        self.driver.find_element(By.CSS_SELECTOR, self.next_page_css).click()
        self.scrollDown()

    def appendGoodsList(self, g):
        super().appendGoodsList(g)
        k = 'href'
        v = "https:" + g('div.content--CUnfXXxv > div > div > a').attr['href']
        self.data.write(k, v)
        k = 'keywords'
        v = self.keywords
        self.data.write(k, v)


def makeCrawl(keywords: list[str], page=30, type="JD") -> (dict, int):
    """
    一次执行爬虫程序,
    可选的type列表['JD','TB']
    JD: www.jd.com 的爬虫
    TB: www.taobao.com 的爬虫
    :param keywords: 搜索关键词字典
    :param page: 搜索页数 默认30页
    :param type: 搜索类型 默认JD
    :return: 一个数据字典，以及爬取数据个数
    """
    try:
        switch = {
            "JD": JDCrawler,
            "TB": TBCrawler
        }
        crw = switch[type]("type")
        crw.searchKeyWords(keywords)
        dt = crw.getDictOfGoods(page)
        return len(dt)
    except Exception as e:
        raise RuntimeError(e)


if __name__ == '__main__':
    r = makeCrawl(['手机'], 1)
    print(r)
