import csv
import os


def save_to_csv(dt, goods):
    csv_file = f'{os.getcwd()}/data/{goods}.csv'  # 使用当前工作目录
    fieldnames = ['爬取时间', '名称', '销售数量', '价格', '店铺省份', '所属店铺']
    try:
        # 确保目录存在
        if not os.path.exists(os.path.dirname(csv_file)):
            os.makedirs(os.path.dirname(csv_file))

        with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            # 假设每个字段的列表长度相同，遍历第一个列表的长度
            for i in range(len(dt['crawlTime'])):
                row_data = {
                    '爬取时间': dt['crawlTime'][i],
                    '名称': dt['name'][i],
                    '销售数量': dt['commentCount'][i],
                    '价格': dt['price'][i],
                    '店铺省份': dt['province'][i],
                    '所属店铺': dt['supplier'][i]
                }
                writer.writerow(row_data)
    except FileNotFoundError as e:
        print(f"无法创建CSV文件：{e}")
    except Exception as e:
        print(f"保存CSV文件时发生错误：{e}")