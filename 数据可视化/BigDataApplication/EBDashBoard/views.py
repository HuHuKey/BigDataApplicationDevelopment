import datetime

from django.shortcuts import render

from .models import Jdnew



# Create your views here.
def dashboard_view(request):
    try:
        sales_data = Jdnew.objects().all()
        context = {'sales_data': sales_data}
        # all_sales_data = SalesData.objects()
        # print("查询到的数据数量:", len(all_sales_data))  # 添加调试输出
    except Exception as e:
        context = {'error_message': f'数据库查询出现问题，请稍后再试{e}'}
    return render(request, 'dash/data.html', context)
