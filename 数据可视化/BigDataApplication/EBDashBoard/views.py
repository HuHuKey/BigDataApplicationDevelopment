import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import HttpResponse
from EBAsite.task import crawl, add
from django_celery_results.models import TaskResult
from utils.crawler.Crawler import makeCrawl
from django.core import serializers

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
        result = []
        for data in sales_data:
            d = data.__dict__()
            d["crawl_time"] = str(d["crawl_time"])
            result.append(d)
        # print(result)
        result = json.dumps(result)
        print(result)
        return HttpResponse(result, content_type='application/json;charset=utf8')
