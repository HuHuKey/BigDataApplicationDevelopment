import warnings

from selenium.webdriver.chrome import webdriver
import json
import time


class CookieSaver:
    __driver: webdriver = None
    __cookies = None
    filename = None

    def __init__(self, driver: webdriver, filename):
        self.__driver = driver
        self.filename = filename

    def get_cookies(self):
        """
        获取当前网页的cookie
        :return:
        """
        self.__cookies = self.__driver.get_cookies()
        print(self.__cookies)

    def save_cookies(self):
        """
        持久化当前网页cookie
        :return:
        """
        with open(self.filename, 'w') as f:
            json.dump(self.__cookies, fp=f, indent=4)

    def load_cookies(self):
        """
        加载持久化cookie
        :return: 是否成功加载cookie
        """
        try:
            with open(self.filename, "r") as fp:
                self.__cookies = json.load(fp)
        except Exception as e:
            warnings.warn(f"加载cookie失败: {e}")
            return False
        if self.is_cookie_empty():
            return False
        try:
            self.__driver.delete_all_cookies()
            for cookie in self.__cookies:
                self.__driver.add_cookie(cookie)
            self.__driver.refresh()
        except Exception as e:
            warnings.warn(f"加载cookie失败: {e}")
            return False
        return True

    def is_cookie_expired(self):
        """
        判断cookie是否过期
        :return: cookie是否过期
        """

        current_time = int(time.time())
        for cookie in self.__cookies:
            if cookie.get('expire', current_time + 1) < current_time:
                return True
        return False

    def is_cookie_empty(self):
        """
        判断cookie是否为空
        :return: cookie是否为空
        """
        return self.__cookies is None or len(self.__cookies) == 0 or self.__cookies == []

    def is_cookie_valid(self):
        """
        判断cookie是否有效
        :return: cookie是否有效
        """
        return not (self.is_cookie_empty() or self.is_cookie_expired())
