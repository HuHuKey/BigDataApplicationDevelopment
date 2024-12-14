import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import HttpResponse
from EBAsite.task import crawl, add
from django_celery_results.models import TaskResult
from utils.crawler.Crawler import makeCrawl
from django.core import serializers
from collections import defaultdict

from .models import Jdnew, Tbnew


# Create your views here.
@login_required
def dashboard_view(request):
    try:
        sales_data = Jdnew.objects().all()[:]
        sales_data_tb = Tbnew.objects().all()[:]
        context = {'sales_data': sales_data,
                   'sales_data_tb': sales_data_tb
                   }
        # 找到grossSales最大，price最低，commentCnt最多的对应的数据
        gross_sale_max = max(sales_data, key=lambda x: x.grossSales)
        price_min = min(sales_data, key=lambda x: x.price)
        comment_cnt_max = max(sales_data, key=lambda x: x.commentCnt)
        context['gross_sale_max'] = gross_sale_max
        context['price_min'] = price_min
        context['comment_cnt_max'] = comment_cnt_max
        # sales_data爬取的数据条数
        length_jd = len(sales_data)
        context['length'] = length_jd
        # 统计每个省份出现的次数
        province_cnt = defaultdict(int)
        for data in sales_data_tb:
            province_cnt[data.province] += 1
        context['province_cnt'] = province_cnt
        # all_sales_data = SalesData.objects()
        # print("查询到的数据数量:", len(all_sales_data))  # 添加调试输出
    except Exception as e:
        context = {'error_message': f'数据库查询出现问题，请稍后再试{e}'}
    return render(request, 'dash/index.html', context)


@login_required
def start_crawl(request):
    if request.method == "POST":
        keywords = request.POST.get('keywords')
        keywords = list(set(keywords.split(',')))
        page = request.POST.get('page')
        type = request.POST.get('type')
        # async_crawl = crawl.delay(keywords, 1)
        task = crawl.delay(keywords, int(page), type)
        # print(keywords, page, type)
        # task = add.delay(1, 2)
        result = {
            "status": "success",
            "message": "成功创建爬虫任务",
            "id": task.task_id
        }
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json;charset=utf8')
    else:
        return render(request, "profile.html")


@login_required
def get_task_status(request):
    if request.method == "GET":
        task = TaskResult.objects.all()
        all = task.count()
        success = task.filter(status="SUCCESS").count()
        failed = task.filter(status="FAILURE").count()
        pending = task.filter(status="PENDING").count()
        active = task.filter(status="ACTIVE").count()
        result = {
            'all': all,
            'success': success,
            'failed': failed,
            'pending': pending,
            'active': active,
            'tasks': task,
        }
        return render(request, 'task/TaskStatus.html', result)


@login_required
def post_data(request):
    if request.method == "POST":
        sales_data = Jdnew.objects().all()[:]
        result = sales_data.to_json()
        # print(result)
        result = json.dumps(result)
        print(result)
        return HttpResponse(result, content_type='application/json;charset=utf8')

def post_data_tb(req):
    if req.method == 'POST':
        sales_data_tb = Tbnew.objects().all()[:]
        res = sales_data_tb.to_json()
        res = json.dumps(res)
        return HttpResponse(res, content_type='application/json;charset=utf8')
