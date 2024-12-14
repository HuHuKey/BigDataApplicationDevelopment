import time
from celery import shared_task
from utils.crawler.Crawler import makeCrawl
from EBAsite.celery import app


@app.task
def crawl(keywords: list[str], page: str = 30, type: str = 'JD'):
    return makeCrawl(keywords, page, type)


@shared_task
def add(a, b):
    return a + b
