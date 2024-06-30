from django.shortcuts import render
from .script import scrape_imdb_news
from django.http import JsonResponse
from .models import News
from home.tasks import add


def run_scraper(request):
    scrape_imdb_news()
    return JsonResponse({
        "status" : True,
        "message" : "scraper executed"
    })


def index(request):
    result  = add.delay(10, 5)
    print(result)
    return render(request, 'index.html', context={
        "news_data" : News.objects.all()
    })