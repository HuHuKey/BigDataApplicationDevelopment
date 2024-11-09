import pymongo
import requests
from bs4 import BeautifulSoup
import time
import re
from pymongo import MongoClient
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
        'Cookie': '__jdu=1725290974438544156666; '
                  'shshshfpa=b523839c-6601-3485-88b3-f3cbf91efc3d-1725290976; '
                  'shshshfpx=b523839c-6601-3485-88b3-f3cbf91efc3d-1725290976; '
                  'jsavif=1; __jdv=143920055|direct|-|none|-|1731115373872; '
                  'areaId=15; _pst=%E6%B3%BDuyh; unick=p3tzq917v8x83s; '
                  'pin=%E6%B3%BDuyh;''thor=BF6F02712229FF6C53C6C9D8823F98ECC2AA'
                  '7B44A6EA1FE8E78387FA6B5BCBF775FB6157DA47C527B58D9D6CD9BC137ED'
                  'F09A760CF4157C6016D8B2F5F47AB144E1D7522B18027E04F65BF3E35978F'
                  'E1DD3AB32AC599EBDAF11E89EBF27BA167135AADD228CC3D969C8165888232'
                  'F639E9FB1DCE893B4B86E2FF49D27C4E39C9; _tp=ZkM%2FJViKyBwD3Bf5AxiWnQ%3D%3D; '
                  'pinId=MRdk9CAU1gw; ipLoc-djd=15-1233-4342-0; o2State={%22webp%22:true%2C%22avif%22:true}; '
                  'PCSYCityID=CN_330000_330300_0; UseCorpPin=%E6%B3%BDuyh; umc_count=2; '
                  'flash=3_duHu8Byl7DoO3xGCTnLbAleBitGiF65y7PRNTjLAexIXBXRCrXKrA8fPjqS-uI3mVkhvH0P'
                  'nl9v9LUj7SsphSGpjEKJLR5FRlrEMDO6OlLOdvhV3DsLWOBUWADq6b2G8aFeFAbuJjFWOXaO6cYMW4to-sL9jjV**; '
                  '3AB9D23F7A4B3CSS=jdd03OSIF3UVIT6NB3D6CNH7PJ2ZZRQQ2UWTWJ5XTGJ5KQSMJVRGPMGX4LZ2YDL3HFXRKMSAN6L'
                  'RY5BZGCVSNBGHIC3D4HIAAAAMTB2ZUZZAAAAAADBFNW24FH7TUMMX; _gia_d=1; '
                  '3AB9D23F7A4B3C9B=OSIF3UVIT6NB3D6CNH7PJ2ZZRQQ2UWTWJ5XTGJ5KQSMJVRGPMGX4LZ2YDL3HFXRKMSAN6LRY5BZ'
                  'GCVSNBGHIC3D4HI; __jda=76161171.1725290974438544156666.1725290974.1725290976.1731115374.2;'
                  ' __jdb=76161171.18.1725290974438544156666|2.1731115374; __jdc=76161171; '
                  'shshshfpb=BApXSNXK7DfZA1S2MlEbaMTp6mrxC2E3nBmdoDllp9xJ1Ml7iyIC2'
    }
    try:
        r = requests.get(url, timeout=30, headers=head)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "获取URL页面失败"

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
            # if (price == '￥'):
            #     price = '￥' + priceInfo.find('strong')['data-price']
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
            product_info['shop_location'] = None
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
    tplt = "{:4}\t{:16}\t{:8}\t{:16}\t{:16}\t{:16}\t{:16}\t{:16}"
    print(tplt.format("序号", "爬取时间", "价格", "名称", "销售数量", "店铺地点", "所属店铺", "销售总额"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g['crawl_time'] or "", g['product_price'] or "", g['product_name'] or "",
                          g['sale_count'] or "", g['shop_location'] or "", g['shop_name'] or "", g['total_sales'] or ""))

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

        # # 将数据保存为csv文件
        # csv_file = 'jd_data.csv'
        # fieldnames = ['序号', '爬取时间', '价格', '名称', '销售数量', '店铺地点', '所属店铺', '销售总额']
        # with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for index, item in enumerate(all_info, start=1):
        #         row_data = {
        #             '序号': index,
        #             '爬取时间': item['crawl_time'],
        #             '价格': item['product_price'],
        #             '名称': item['product_name'],
        #             '销售数量': item['sale_count'],
        #             '店铺地点': item['shop_location'],
        #             '所属店铺': item['shop_name'],
        #             '销售总额': item['total_sales']
        #         }
        #         writer.writerow(row_data)

    printGoodList(all_info)

main()