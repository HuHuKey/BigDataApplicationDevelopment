from django.shortcuts import render

from .models import SalesData,Jdnew
from utils.mongo.reader import read_jd_goods
from utils.ConnectionPool import Client_Pool


# Create your views here.
def dashboard_view(request):
    def refresh():
        cursor = read_jd_goods(Client_Pool)
        for item in cursor:
            crawl_time = item['crawlTime']
            product_name = item['name']
            product_price = item['price']
            comment_count = item['commentCount']
            SalesData.objects.create(crawl_time=crawl_time, product_name=product_name, product_price=product_price,
                                     comment_count=comment_count)

    try:
        sales_data = Jdnew.objects().all()
        context = {'sales_data': sales_data}
        all_sales_data = SalesData.objects()
        print("查询到的数据数量:", len(all_sales_data))  # 添加调试输出
    except Exception as e:
        context = {'error_message': f'数据库查询出现问题，请稍后再试{e}'}
    return render(request, 'dash/data.html', context)
