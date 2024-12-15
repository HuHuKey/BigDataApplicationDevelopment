from utils.datasaver.MongoSaver import upsertTuple
from utils.ConnectionPool import Client_Pool
from EBAsite.settings import DATABASES
from utils.datasaver.clear import jd_tuple_clear


class CrawlerData:
    dataList: list[dict[str, any]]
    dataDict: dict[str, any]
    cssDict: dict[str, str]

    def __len__(self):
        return len(self.dataList)

    def __init__(self, css_dict: dict[str, str]):
        self.cssDict = css_dict
        self.dataList = []
        self.dataDict = {}

    def write(self, col_name: str, value: any):
        self.dataDict[col_name] = value

    def css(self, name: str) -> str:
        return self.cssDict.get(name, "")

    def nextTuple(self, collection: str):
        for col_name in self.cssDict.keys():
            self.dataDict[col_name] = self.dataDict.get(col_name, None)
        keys = ['name', 'crawlTime']
        upsertTuple(Client_Pool, DATABASES['mongodb']['NAME'], collection, keys, self.dataDict)
        self.dataList.append(self.dataDict)
        self.dataDict.clear()

    def getColName(self):
        return tuple(self.cssDict.keys())


class JDCrawlerData(CrawlerData):
    def nextTuple(self, collection: str):
        for col_name in self.cssDict.keys():
            self.dataDict[col_name] = self.dataDict.get(col_name, None)
        keys = ['name', 'crawlTime']
        success = jd_tuple_clear(self.dataDict)
        if not success:
            self.dataDict.clear()
            return
        upsertTuple(Client_Pool, DATABASES['mongodb']['NAME'], collection, keys, self.dataDict)
        self.dataList.append(self.dataDict)
        self.dataDict.clear()
