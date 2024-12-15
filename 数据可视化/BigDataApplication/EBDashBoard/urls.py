from django.urls import path
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path("start/", views.start_crawl, name="profile"),
    path("start/crawl", views.start_crawl, name="crawl"),
    # path(r'^dash/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
    path("task/", views.get_task_status, name="task"),
    # path("api/getData", views.post_data, name="getData"),
    path("task/<str:task_id>", views.get_task_status, name="task_detail"),
    path("api/data4pie", views.data4pie, name="data4pie"),
    path("api/data4line", views.data4line, name="data4line"),
]
