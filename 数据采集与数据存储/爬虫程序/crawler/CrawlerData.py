class CrawlerData:
    dataList: list[dict[str, any]]
    dataDict: dict[str, any]
    cssDict: dict[str, str]

    def __init__(self, css_dict: dict[str, str]):
        self.cssDict = css_dict
        self.dataList = []
        self.dataDict = {}

    def write(self, col_name: str, value: any):
        self.dataDict[col_name] = value

    def css(self, name: str) -> str:
        return self.cssDict.get(name, "")

    def nextRow(self):
        for col_name in self.cssDict.keys():
            self.dataDict[col_name] = self.dataDict.get(col_name, None)
        self.dataList.append(self.dataDict)
        self.dataDict = {}

    def getColName(self):
        return tuple(self.cssDict.keys())