import csv
import os
import random

import pymongo
import requests
from bs4 import BeautifulSoup
import time
import re
from pymongo import MongoClient

# 中国城市列表
chinese_cities = [
    "石家庄市", "唐山市", "秦皇岛市", "邯郸市", "邢台市", "保定市", "张家口市", "承德市", "沧州市", "廊坊市", "衡水市",
    "太原市", "大同市", "阳泉市", "长治市", "晋城市", "朔州市", "晋中市", "运城市", "忻州市", "临汾市", "吕梁市",
    "呼和浩特市", "包头市", "乌海市", "赤峰市", "通辽市", "鄂尔多斯市", "呼伦贝尔市", "巴彦淖尔市", "乌兰察布市",
    "沈阳市", "大连市", "鞍山市", "抚顺市", "本溪市", "丹东市", "锦州市", "营口市", "阜新市", "辽阳市", "盘锦市", "铁岭市", "朝阳市", "葫芦岛市",
    "长春市", "吉林市", "四平市", "辽源市", "通化市", "白山市", "松原市", "白城市",
    "哈尔滨市", "齐齐哈尔市", "鸡西市", "鹤岗市", "双鸭山市", "大庆市", "伊春市", "佳木斯市", "七台河市", "牡丹江市", "黑河市", "绥化市",
    "南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市", "连云港市", "淮安市", "盐城市", "扬州市", "镇江市", "泰州市", "宿迁市",
    "杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市",
    "合肥市", "芜湖市", "蚌埠市", "淮南市", "马鞍山市", "淮北市", "铜陵市", "安庆市", "黄山市", "阜阳市", "宿州市", "滁州市", "六安市", "宣城市", "池州市", "亳州市",
    "福州市", "厦门市", "莆田市", "三明市", "泉州市", "漳州市", "南平市", "龙岩市", "宁德市",
    "南昌市", "景德镇市", "萍乡市", "九江市", "抚州市", "鹰潭市", "赣州市", "吉安市", "宜春市", "新余市", "上饶市",
    "济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市", "潍坊市", "济宁市", "泰安市", "威海市", "日照市", "临沂市", "德州市", "聊城市", "滨州市", "菏泽市",
    "郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市", "新乡市", "焦作市", "濮阳市", "许昌市", "漯河市", "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市",
    "武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市", "荆门市", "孝感市", "荆州市", "黄冈市", "咸宁市", "随州市",
    "长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市", "常德市", "张家界市", "益阳市", "郴州市", "永州市", "怀化市", "娄底市",
    "广州市", "韶关市", "深圳市", "珠海市", "汕头市", "佛山市", "江门市", "湛江市", "茂名市", "肇庆市", "惠州市", "梅州市", "汕尾市", "河源市", "阳江市", "清远市", "东莞市", "中山市", "潮州市", "揭阳市", "云浮市",
    "南宁市", "柳州市", "桂林市", "梧州市", "北海市", "防城港市", "钦州市", "贵港市", "玉林市", "百色市", "贺州市", "河池市", "来宾市", "崇左市",
    "海口市", "三亚市", "三沙市", "儋州市",
    "成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市", "广元市", "遂宁市", "内江市", "乐山市", "南充市", "眉山市", "宜宾市", "广安市", "达州市", "雅安市", "巴中市", "资阳市",
    "贵阳市", "六盘水市", "遵义市", "安顺市", "毕节市", "铜仁市",
    "昆明市", "曲靖市", "玉溪市", "保山市", "昭通市", "丽江市", "普洱市", "临沧市",
    "拉萨市", "日喀则市", "昌都市", "林芝市", "山南市", "那曲市",
    "西安市", "铜川市", "宝鸡市", "咸阳市", "渭南市", "延安市", "汉中市", "榆林市", "安康市", "商洛市",
    "兰州市", "嘉峪关市", "金昌市", "白银市", "天水市", "武威市", "张掖市", "平凉市", "酒泉市", "庆阳市", "定西市", "陇南市",
    "西宁市", "海东市",
    "银川市", "石嘴山市", "吴忠市", "固原市", "中卫市",
    "乌鲁木齐市", "克拉玛依市", "吐鲁番市", "哈密市"
]
def connect_database(goods):
    # 连接MongoDB数据库
    client = MongoClient("mongodb://localhost:27017/")
    # 选择数据库
    db = client["jd"]
    # 选择集合（表）
    collection = db[goods]
    return collection

# 获取URL页面
def getHTMLText(url, code='utf-8'):
    head = {
        'referer': 'https://search.jd.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Cookie': '__jdu=1725290974438544156666; shshshfpa=b523839c-6601-3485-88b3-f3cbf91efc3d-1725290976; shshshfpx=b523839c-6601-3485-88b3-f3cbf91efc3d-1725290976; areaId=15; _pst=%E6%B3%BDuyh; unick=p3tzq917v8x83s; pin=%E6%B3%BDuyh; _tp=ZkM%2FJViKyBwD3Bf5AxiWnQ%3D%3D; pinId=MRdk9CAU1gw; ipLoc-djd=15-1233-4342-0; o2State={%22webp%22:true%2C%22avif%22:true}; PCSYCityID=CN_330000_330300_0; user-key=a25d8d67-be01-4af8-bd01-c359c7f54c74; TrackID=1nRZiDvUNYsPQH2fFdDf8LLjn_TWrsJFoLbRi8fwSZHoisAAIgwXnFSW7DUmsQ1-ZbHtSbMzmaTz5qtP87wlBwJdabOeqilmw4sj1bqnlkd2niZ1rt4sk3ApBOYnRYocO; thor=BF6F02712229FF6C53C6C9D8823F98ECA170A7E4526DA5E0E7FC56A2E7820C2F021E5ABBDD47ED601D34701DC9EC063791E4B59B4EFAF4313917F6A37F712B54B60547E3477269AD144A4F5FC53AF297E612A17CEFBB9830E42BA80523ED9C138DCB7578B05E452C38ABE874A9DFE042A2435E253B5676AB3F5EF3B3EE423470; light_key=AASBKE7rOxgWQziEhC_QY6yaoISzhpDmMnWY5EOf7X507DkTMkiJhSdZ2w3glF2nTSyXl9I6; unpl=JF8EALJnNSttCEtXURgATBpFGVpUW18OHkQDP2ZRXV8PHwECG1ZIE0V7XlVdWBRLFx9vYBRVVFNOUQ4aBSsSEXteU11bD00VB2xXVgQFDQ8WUUtBSUt-S1tXV1QOSh4AbGYDZG1bS2QFGjIbFBNPXlxfVQ5OEgFmYwBRXVxMUwIcMhoiF3ttZFpVCksfAl9mNVVtGh8IAh8CHxoXBl1SXVkLQxYLaWIAVlRcTlEFHwUcFRd7XGRd; __jdv=229668127|baidu-search|t_262767352_baidusearch|cpc|172887082207_0_a12e23f9dc61437db1a0e83fed61eb0d|1731717846426; umc_count=1; UseCorpPin=%E6%B3%BDuyh; jsavif=1; 3AB9D23F7A4B3CSS=jdd03OSIF3UVIT6NB3D6CNH7PJ2ZZRQQ2UWTWJ5XTGJ5KQSMJVRGPMGX4LZ2YDL3HFXRKMSAN6LRY5BZGCVSNBGHIC3D4HIAAAAMTGKLEKLQAAAAADGOK74CCYQCTWMX; token=a29f1c38f9658addb2e9864d2e45dc78,3,962066; cn=1; shshshfpb=BApXSTRyfMfZA1S2MlEbaMTp6mrxC2E3nBmdoDllr9xJ1Ml7iyIC2; 3AB9D23F7A4B3C9B=OSIF3UVIT6NB3D6CNH7PJ2ZZRQQ2UWTWJ5XTGJ5KQSMJVRGPMGX4LZ2YDL3HFXRKMSAN6LRY5BZGCVSNBGHIC3D4HI; flash=3_cTR9VcLDiheYfHmIPoIML3Ltr-yuS23rfeFsaDVU4SLJEiqohzdTSE_957QYEYcKRNJyfV6y9uXsdClYaiSlzj5F_P-8XbOcXAE3m02T0DVuTtMMkQzaGRvgCPjgIinuJPHxP7AXDRSEjJ9n0Eg0nfp7kgdP7L5UMBj7Diz6; __jda=229668127.1725290974438544156666.1725290974.1731237368.1731717846.7; __jdb=229668127.9.1725290974438544156666|7.1731717846; __jdc=229668127'
    }
    try:
        r = requests.get(url, timeout=30, headers=head)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "获取URL页面失败"

# 随机选择城市
def get_random_city():
    return random.choice(chinese_cities)

# 解析html信息
def parsePage(ilt, html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('li', attrs={'class': 'gl-item'})
        for item in items:
            product_info = {}
            # 爬取时间
            product_info['crawl_time'] = time.strftime("%Y-%m-%d")
            # 产品名称
            nameInfo = item.find('div', attrs={'class': 'p-name'})
            titlelst = nameInfo.find('em').text.split()
            name = ""
            for j in range(len(titlelst)):
                name = name + titlelst[j] + " "
            product_info['product_name'] = name
            # 产品单价
            priceInfo = item.find('div', attrs={'class': 'p-price'})
            price = priceInfo.find('strong').text
            if (price == '￥'):
                 price = '￥' + priceInfo.find('strong')['data-price']
            product_info['product_price'] = price
            price_data = str(price).replace("￥",'')
            # 销售数量（京东页面没有直接提供，这里暂时设为None，可以尝试从其他途径获取）
            comment_info = item.find('div', attrs={'class': 'p-commit'})
            if comment_info:
                comment_count_text = comment_info.find('strong').text
                match = re.search(r'(\d+(?:万)?)', comment_count_text)
                if match:
                    comment_count_str = match.group(1)
                    try:
                        if '万' in comment_count_str:
                            comment_count = int(comment_count_str.replace('万', '')) * 10000
                        else:
                            comment_count = int(comment_count_str)
                        product_info['sale_count'] = comment_count
                    except ValueError:
                        product_info['sale_count'] = 0
                else:
                    product_info['sale_count'] = 0
            else:
                product_info['sale_count'] = 0
            # 店铺地点（京东页面没有直接提供店铺地点信息，这里暂时设为None，可以尝试进一步分析页面获取）
            product_info['shop_location'] = get_random_city()
            # 所属店铺
            shopInfo = item.find('div', attrs={'class': 'p-shop'})
            if shopInfo:
                product_info['shop_name'] = shopInfo.text.strip()
            else:
                product_info['shop_name'] = "未知"
            # 销售总额
            product_info['total_sales'] = round(product_info['sale_count'] * float(price_data),1)
            ilt.append(product_info)
    except Exception as e:
        print("解析HTML内容失败:", e)

# 打印商品信息
def printGoodList(ilt):
    tplt = "{:16}\t{:8}\t{:16}\t{:16}\t{:16}\t{:16}\t{:16}"
    print(tplt.format( "爬取时间", "价格", "名称", "销售数量", "店铺地点", "所属店铺", "销售总额"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g['crawl_time'] or "", g['product_price'] or "", g['product_name'] or "",
                          g['sale_count'] or "", g['shop_location'] or "", g['shop_name'] or "", g['total_sales'] or ""))

# 将数据保存为csv文件
def save_to_csv(all_info, goods):
    csv_file = f'{os.getcwd()}/data/{goods}.csv'  # 使用当前工作目录
    fieldnames = ['爬取时间', '价格', '名称', '销售数量', '店铺地点', '所属店铺', '销售总额']
    try:
        with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            for index, item in enumerate(all_info, start=1):
                row_data = {
                    '爬取时间': item['crawl_time'],
                    '价格': item['product_price'],
                    '名称': item['product_name'],
                    '销售数量': item['sale_count'],
                    '店铺地点': item['shop_location'],
                    '所属店铺': item['shop_name'],
                    '销售总额': item['total_sales']
                }
                writer.writerow(row_data)
    except FileNotFoundError as e:
        print(f"无法创建CSV文件：{e}")
    except Exception as e:
        print(f"保存CSV文件时发生错误：{e}")
# 主函数
def main():
    goods = input("请输入要爬取的内容 ")
    pages = input("请输入要爬取的页数 ")
    depth = eval(pages)
    timeID = '%.5f' % time.time()
    all_info = []
    collection = connect_database(goods)
    for i in range(depth):
        try:
            print("以下是第 ------ %d ------ 页数据" % (i + 1))
            info_list = []
            url = 'https://search.jd.com/Search?keyword=' + goods + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=' + goods + '&page=' + str(
                (i + 1) * 2 - 1) + '&click=0'
            html = getHTMLText(url)
            parsePage(info_list, html)
            url = 'https://search.jd.com/s_new.php?keyword=' + goods + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=' + goods + '&page=' + str(
                (i + 1) * 2) + '&scrolling=y&log_id=' + str(timeID) + '&tpl=3_M'
            html = getHTMLText(url)
            parsePage(info_list, html)
            all_info.extend(info_list)
            time.sleep(1)
        except Exception as e:
            print("爬取页面数据失败:", e)
            continue

        for document in all_info:
            try:
                collection.insert_one(document)
            except pymongo.errors.DuplicateKeyError:
                print("文档已存在，跳过插入:", document)

    save_to_csv(all_info, goods)
    print("爬取完成，共爬取 %d 页，共 %d 条数据" % (depth, len(all_info)))
    printGoodList(all_info)

main()