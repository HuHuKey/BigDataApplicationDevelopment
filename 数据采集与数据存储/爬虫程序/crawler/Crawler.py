import warnings
from abc import ABCMeta, abstractmethod

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .cookies.CookieSaver import CookieSaver
from selenium.webdriver.edge.options import Options

from pyquery import PyQuery as pq


class Crawler(metaclass=ABCMeta):
    """爬虫的抽象基类，包含抽象方法"""
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
    """
    基本的泛型爬虫类


    Attributes:
        name: str               爬虫类的名称(暂时没用)
        url: str                爬虫类爬取的url
        driver: webdriver       爬虫类的webdriver(Chrome, Edge, Firefox ...)
        col2css: dict[str, str] 字段名到css选择器的映射比如{'name': 'div.p-name.p-name-type-2 > a > em'}就表示name字段对应的css选择器，设置完就可以直接爬取了
        goods_css: str          商品的css选择器，就是网页上商品元素的css选择器
        search_bar: str         搜索框的css选择器，比如京东首页的input框
        max_page_css: str       最大页数的css选择器(非必须),比如搜索后搜索结果的最下面
        next_page_css: str      下一页的css选择器
        options: Options        webDriver选项
    """
    name = None
    url = None
    driver: webdriver = None
    col2css: dict[str, str]
    goods_css = None
    search_bar = None
    max_page_css = None
    next_page_css = None
    options: Options = None

    def __init__(self, name: str,
                 url: str,
                 search_bar="input[type='text']",
                 max_page_css='#J_bottomPage > span.p-skip > em:nth-child(1) > b',
                 goods_css: str = '#J_goodsList > ul > li',
                 next_page_css='KEY.RIGHT',
                 options: Options = None,
                 col2css: dict[str, str] = None,
                 ):
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
        self.options = options
        self.goods_css = goods_css
        self.search_bar = search_bar
        self.max_page_css = max_page_css
        self.next_page_css = next_page_css
        self.driver = webdriver.Edge(options=options)
        self.driver.get(url)

    def searchKeyWords(self, keywords: list):
        try:
            (WebDriverWait(self.driver, 10)
            .until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.search_bar))))
        except Exception as e:
            warnings.warn(f"无法找到搜索框，请检查网络:{e}")
            return

        text_input = self.driver.find_element(By.CSS_SELECTOR, self.search_bar)
        text_input.send_keys(" ".join(keywords))
        text_input.send_keys(webdriver.Keys.RETURN)

    def __collectGoodsData(self, goods: str) -> dict[str, list[str]]:
        data_list = dict(zip(self.col2css.keys(), [[] for _ in self.col2css.keys()]))
        for good in goods:
            for (k, v) in self.col2css.items():
                g = pq(good)
                try:
                    element = g(v).eq(0)
                    data_list[k].append(element.text())
                except Exception as e:
                    print(e)
        return data_list

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
        return self.__collectGoodsData(goods)

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

    def getDictOfGoods(self, page_num: int = 30) -> dict[str, list[str]]:
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.max_page_css)))
            total_page = self.driver.find_element(By.CSS_SELECTOR, self.max_page_css).text
        except Exception as e:
            warnings.warn(f"无法找到maxPageNum:{e},使用默认参数total_page=100")
            total_page = 100
        total_page = int(total_page)
        data_list = dict(zip(self.col2css.keys(), [[] for _ in self.col2css.keys()]))
        for _ in range(min(page_num, total_page)):
            new_goods = self.getOnePageOfGoods()
            for col in self.col2css.keys():
                data_list[col].extend(new_goods[col])
            self.turnToNextPage()
        return data_list

    def close(self):
        self.driver.close()

    def getDataFrameOfGoods(self, page_num: int = 30) -> pd.DataFrame:
        goods = self.getDictOfGoods(page_num)
        df = pd.DataFrame(goods)
        return df

    # TODO: 添加一个进入链接，实现爬取评论的方法或者类
    def getComments(self):
        pass


class CookieCrawler(BaseCrawler):
    @abstractmethod
    def turnToNextPage(self):
        pass

    __cookie_saver: CookieSaver = None

    def __init__(self, cookie_filename: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        file = cookie_filename.split('/')
        file[-1] = self.url.replace("://", "_") + '_' + file[-1]
        cookie_filename = '/'.join(file)

        self.__cookie_saver = CookieSaver(self.driver, cookie_filename)

        not_load = not self.__cookie_saver.load_cookies()
        invalid = not self.__cookie_saver.is_cookie_valid()

        while not_load or invalid:
            # TODO: 这里可以改成一个Web交互式界面
            input("Cookie is failed to load, please press 'Enter' after login.")
            self.__cookie_saver.get_cookies()
            self.__cookie_saver.save_cookies()
            not_load = not self.__cookie_saver.load_cookies()
            invalid = not self.__cookie_saver.is_cookie_valid()

    def getDataFrameOfGoods(self, page_num: int = 30) -> pd.DataFrame:
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.max_page_css)))
        return super().getDataFrameOfGoods(page_num)


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
        options.page_load_strategy = "none"
        super().__init__(*args, options=options, **kwargs)


class JDCrawler(HeadlessCrawler):
    def __init__(self, name: str, url: str, cookie_filename: str):
        args = (cookie_filename, name, url)
        kwargs = {
            "col2css": {
                "name": 'div.p-name.p-name-type-2 > a > em',
                "price": 'div.p-price > strong > i',
                "supplier": 'div.p-shop > span > a',
                "comment_num": 'div.p-commit > strong > a'
            },
            "goods_css": '#J_goodsList > ul > li',
            "search_bar": 'input[type="text"]',
            "max_page_css": '#J_bottomPage > span.p-skip > em:nth-child(1) > b',
            'next_page_css': 'KEY.RIGHT'
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

# TODO: 添加一个泛型爬虫，可以通过用户自定义爬取网站信息。
