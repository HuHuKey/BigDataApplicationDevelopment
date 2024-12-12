from django.urls import path
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path("start/", views.start_crawl, name="profile"),
    path("start/crawl", views.start_crawl, name="crawl"),
    path(r'^dash/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
]
