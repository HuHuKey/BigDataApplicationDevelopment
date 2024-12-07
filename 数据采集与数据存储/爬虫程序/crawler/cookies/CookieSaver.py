import warnings

from selenium.webdriver.chrome import webdriver
import json
import time
import pymongo


class Cookie:
    domain = None
    content = None

    def __init__(self, domain: str, content: dict = None, method="mongodb"):
        self.domain = domain
        if self.content is None:
            switch = {
                "mongodb": self.read_mongoDB,
                "json": self.read_json,
            }
            switch.get(method)()
        else:
            self.content = content

    def to_dict(self):
        return {self.domain: self.content}

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def is_cookie_expired(self):
        """
        判断cookie是否过期
        :return: cookie是否过期
        """

        current_time = int(time.time())
        for cookie in self.content:
            if cookie.get('expire', current_time + 1) < current_time:
                return True
        return False

    def is_cookie_empty(self):
        """
        判断cookie是否为空
        :return: cookie是否为空
        """
        return self.content is None or len(self.content) == 0 or self.content == []

    def is_cookie_valid(self):
        """
        判断cookie是否有效
        :return: cookie是否有效
        """
        return not (self.is_cookie_empty() or self.is_cookie_expired())

    def to_mongoDB(self, host="mongodb://localhost:27017/", database="cookie", collection="cookies"):
        with pymongo.MongoClient(host) as client:
            db = client[database]
            collection = db[collection]
            collection.update_one({'domain': self.domain}, {'$set': {'content': self.content}}, upsert=True)

    def read_mongoDB(self, host="mongodb://localhost:27017/", database="cookie", collection="cookies"):
        with pymongo.MongoClient(host) as client:
            db = client[database]
            collection = db[collection]
            result = collection.find_one({'domain': self.domain})
            if result is not None:
                self.content = result['content']

    def read_json(self, filepath):
        with open(filepath, "r") as fp:
            self.content = json.load(fp)


class CookieSaver:
    __driver: webdriver = None
    __cookies: Cookie = None
    filename = None

    def __init__(self, driver: webdriver):
        self.__driver = driver
        self.__cookies = Cookie(self.get_current_domain())

    def refresh_cookies(self):
        """
        获取当前网页的cookie
        :return:
        """
        self.refresh_domain()
        self.__cookies.content = self.__driver.get_cookies()

    def get_current_domain(self):
        domain = self.__driver.execute_script("return window.location.hostname;")
        domain = domain.replace("www.", "")
        return domain

    def refresh_domain(self):
        self.__cookies.domain = self.get_current_domain()

    # TODO: 实现cookie的mongoDB存取
    # TODO: 以{'url':'cookie'}的形式存储cookie,以{'url':'cookie'}的形式加载cookie
    def save_cookies(self, method="mongodb"):
        """
        持久化当前网页cookie,用mongoDB存储，文件存储不安全，已弃用
        :return:
        """
        self.refresh_cookies()
        self.__cookies.to_mongoDB()

    def load_cookies(self):
        """
        加载持久化cookie
        :return: 是否成功加载cookie
        """
        self.__cookies.read_mongoDB()
        # try:
        #     with open(self.filename, "r") as fp:
        #         self.__cookies = json.load(fp)
        # except Exception as e:
        #     warnings.warn(f"加载cookie失败: {e}")
        #     return False
        if self.__cookies.is_cookie_empty():
            return False
        try:
            self.__driver.delete_all_cookies()
            for cookie in self.__cookies.content:
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
        return self.__cookies.is_cookie_expired()

    def is_cookie_empty(self):
        """
        判断cookie是否为空
        :return: cookie是否为空
        """
        return self.__cookies.is_cookie_empty()

    def is_cookie_valid(self):
        """
        判断cookie是否有效
        :return: cookie是否有效
        """
        return self.__cookies.is_cookie_valid()

    @property
    def cookies(self):
        return self.__cookies
