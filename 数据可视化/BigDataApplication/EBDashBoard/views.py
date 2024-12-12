import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import HttpResponse
from utils.crawler.Crawler import makeCrawl

from .models import Jdnew


# Create your views here.
@login_required
def dashboard_view(request):
    try:
        sales_data = Jdnew.objects().all()
        context = {'sales_data': sales_data}
        # all_sales_data = SalesData.objects()
        # print("查询到的数据数量:", len(all_sales_data))  # 添加调试输出
    except Exception as e:
        context = {'error_message': f'数据库查询出现问题，请稍后再试{e}'}
    return render(request, 'dash/data.html', context)


@login_required
def start_crawl(request):
    if request.method == "POST":
        keywords = request.POST.get('keywords')
        print(keywords)
        keywords = list(set(keywords.split(',')))
        print(keywords)
        crawl = makeCrawl(keywords, 1)
        result = {
            "status": "success",
            "message": "爬取成功",
            "datalist": crawl[0],
            "count": crawl[1]
        }
        print(result)
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json;charset=utf8')
    else:
        return render(request, "profile.html")
