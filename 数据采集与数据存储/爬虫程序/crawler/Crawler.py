import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .cookies.CookieSaver import CookieSaver
from selenium.webdriver.edge.options import Options


class BaseCrawler:
    __url = None
    driver: webdriver = None

    def __init__(self, url: str, options: Options = None):
        self.__url = url
        if options is None:
            options = Options()
        self.driver = webdriver.Edge(options=options)
        self.driver.get(url)

    def searchKeyWords(self, keywords: list):
        text_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        text_input.send_keys(" ".join(keywords))
        text_input.send_keys(webdriver.Keys.RETURN)

    def getOnePageOfGoods(self):
        goods = self.driver.find_elements(By.CSS_SELECTOR, '#J_goodsList > ul > li')
        names = []
        prices = []
        suppliers = []
        for good in goods:
            name = good.find_element(By.CSS_SELECTOR, 'div.p-name.p-name-type-2 > a > em').text
            price = good.find_element(By.CSS_SELECTOR, 'div.p-price > strong > i').text
            supplier = good.find_element(By.CSS_SELECTOR, 'div.p-shop > span > a').text
            names.append(name)
            prices.append(price)
            suppliers.append(supplier)
        return {"name": names, "price": prices, "supplier": suppliers}

    def turnToNextPage(self):
        """
        只适用于京东，翻页
        :return: None
        """
        body = self.driver.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(webdriver.Keys.RIGHT)
        self.scrollDown()

    def scrollDown(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def getDataFrameOfGoods(self, page_num: int = 30) -> pd.DataFrame:
        total_page = self.driver.find_element(
            By.CSS_SELECTOR,
            '#J_bottomPage > span.p-skip > em:nth-child(1) > b').text
        goods = {"name": [], "price": [], "supplier": []}
        total_page = int(total_page)
        for _ in range(min(page_num, total_page)):
            new_goods = self.getOnePageOfGoods()
            for key in goods.keys():
                goods[key].extend(new_goods[key])
            self.turnToNextPage()
        df = pd.DataFrame(goods)
        return df


class CookieCrawler(BaseCrawler):
    __cookie_saver: CookieSaver = None

    def __init__(self, cookie_filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cookie_saver = CookieSaver(self.driver, cookie_filename)

        not_load = not self.__cookie_saver.load_cookies()
        invalid = not self.__cookie_saver.is_cookie_valid()

        if not_load or invalid:
            input("Cookie is failed to load, please press enter after login.")
            self.__cookie_saver.get_cookies()
            self.__cookie_saver.save_cookies()
            self.__cookie_saver.load_cookies()

    def getDataFrameOfGoods(self, page_num: int = 30) -> pd.DataFrame:
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b")))
        return super().getDataFrameOfGoods(page_num)


class HeadlessCrawler(CookieCrawler):
    def __init__(self, *args, **kwargs):
        options = Options()
        options.add_argument("--headless")
        super().__init__(*args, options=options, **kwargs)
