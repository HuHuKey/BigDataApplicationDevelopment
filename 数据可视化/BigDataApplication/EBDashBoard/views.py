import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import HttpResponse
from mongoengine import Q
from django.db.models import Avg
from pymongo import MongoClient
from EBAsite.task import crawl, add
from django_celery_results.models import TaskResult

from .models import Jdnew, Tbnew, Jd


# Create your views here.
@login_required
def dashboard_view(request):
    try:
        sales_data = Jdnew.objects().order_by('-crawlTime').limit(30)
        sales_data_tb = Tbnew.objects().order_by('-crawlTime').limit(30)
        origin_jd = Jd.objects().order_by("-CrawlTime").limit(30)
        context = {
            'sales_data': sales_data,
            'sales_data_tb': sales_data_tb,
            'origin_jd': origin_jd
        }
        # print(origin_jd.to_json())
        # 找到grossSales、price、commentCnt最值
        gross_sale_max = max(sales_data, key=lambda x: x.grossSales)
        price_min = min(sales_data, key=lambda x: x.price)
        comment_cnt_max = max(sales_data, key=lambda x: x.commentCnt)
        gross_sale_min = min(sales_data, key=lambda x: x.grossSales)
        price_max = max(sales_data, key=lambda x: x.price)
        comment_cnt_min = min(sales_data, key=lambda x: x.commentCnt)
        context['gross_sale_max'] = gross_sale_max
        context['price_min'] = price_min
        context['comment_cnt_max'] = comment_cnt_max
        context['gross_sale_min'] = gross_sale_min
        context['price_max'] = price_max
        context['comment_cnt_min'] = comment_cnt_min
        # sales_data爬取的数据条数
        length = Jdnew.objects().count() + Tbnew.objects().count()
        context['length'] = length
        # 得分统计
        scored_data = []
        for data in sales_data:
            price_score = 100 - 40 * (data.price - price_min.price) / (price_max.price - price_min.price)
            gross_sale_score = 100 - 40 * (data.grossSales - gross_sale_min.grossSales) / (
                    gross_sale_max.grossSales - gross_sale_min.grossSales)
            comment_cnt_score = 100 - 40 * (data.commentCnt - comment_cnt_min.commentCnt) / (
                    comment_cnt_max.commentCnt - comment_cnt_min.commentCnt)
            final_score = 0.2 * price_score + 0.2 * gross_sale_score + 0.6 * comment_cnt_score
            scored_data.append((data, final_score))
        scored_data.sort(key=lambda x: x[1], reverse=True)
        top_six = []
        for item in scored_data[:6]:
            top_six.append({'name': item[0].name, 'score': item[1], 'href': item[0].href})
        context['top_six'] = top_six
        # print(sales_data.to_json())
        # all_sales_data = SalesData.objects()
        # print("查询到的数据数量:", len(all_sales_data))  # 添加调试输出
    except Exception as e:
        context = {'error_message': f'数据库查询出现问题，请稍后再试{e}'}
    return render(request, 'dash/index.html', context)


@login_required()
def avgSale4pie(req):
    if req.method == 'POST':
        pipeline = [
            {
                "$group": {
                    "_id": "$crawlTime",
                    "average_total_sales": {"$avg": "$gross sales"}
                }
            },
            {
                "$sort": {
                    "_id": 1  # 按照_id（也就是crawlTime）进行降序排序，使得时间从近到远
                }
            }
        ]
        average_daily_sales_result = Jdnew.objects().aggregate(pipeline)
        res = json.dumps(list(average_daily_sales_result))
        return HttpResponse(res, content_type='application/json;charset=utf8')


def keywords_view(request, keyword):
    try:
        sales_data = Jdnew.objects(keywords=keyword)[:30]
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
        sales_data = Jdnew.objects().filter(Q(keywords__contains="打印"))
        result = sales_data.to_json()
        # print(result)
        return HttpResponse(result, content_type='application/json;charset=utf8')


def post_data_tb(req):
    if req.method == 'POST':
        sales_data_tb = Tbnew.objects().all()[:]
        res = sales_data_tb.to_json()
        res = json.dumps(res)
        return HttpResponse(res, content_type='application/json;charset=utf8')


@login_required
def data4pie(req):
    if req.method == 'POST':
        pipeline = [
            {
                "$group": {
                    "_id": "$province",
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
        province_cnt = Tbnew.objects().aggregate(pipeline)
        res = json.dumps(list(province_cnt))
        return HttpResponse(res, content_type='application/json;charset=utf8')


@login_required()
def data4line(req):
    if req.method == 'POST':
        pipeline = [
            {
                "$group": {
                    "_id": "$crawlTime",  # 按照crawlTime进行分组，将crawlTime的值作为分组的_id
                    "averageCommentCount": {"$avg": "$commentCount"},  # 计算每组中commentCount的平均数
                    "averagePrice": {"$avg": "$price"},  # 计算每组中commentCount的平均数
                }
            },
            {
                "$sort": {
                    "_id": 1  # 按照_id（也就是crawlTime）进行降序排序，使得时间从近到远
                }
            }
        ]
        res = Jdnew.objects().aggregate(pipeline)
        res = json.dumps(list(res))
        return HttpResponse(res, content_type='application/json;charset=utf8')


@login_required
def data4desc(req):
    if req.method == 'POST':
        total = Jdnew.objects().count() + Tbnew.objects().count()
