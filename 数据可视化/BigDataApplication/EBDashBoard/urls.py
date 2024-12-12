from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path("start/", views.start_crawl, name="profile"),
    path("start/crawl", views.start_crawl, name="crawl"),
]
