from concurrent.futures import thread
import json

import threading
from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from playwright.sync_api import sync_playwright
from scrapy import Selector
import main_app.brands
from main_app.models import Media

import csv


# Create your views here.
def main_page(req):
    return render(req, 'main_page.html')


# @sync_to_async
def data_insert(req: WSGIRequest):
    a = dict(req.POST)
    data = []
    for i in a.keys():
        i = str(i)
        if i.startswith('data'):
            data += (a[i])
    print(data)
    p = ''
    models = []
    for i in data:
        i: str
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(i, timeout=120 * 1000)
            p = (page.inner_html('html'))
            # with open("x.html"  ,"w")as f:
            #     f.write(str(p))
            x = Selector(text=p)
            b = main_app.brands.Brands(x, i)
            model = (b.start())
            models.append(model)
            print("models: ",model)
            print("started " + i)
            x = threading.Thread(target=get_all_users, args=(model,))
            x.start()
    print(100*"$")
    print(models)
    return render(req, "insert_data_page.html", {"m": {'data': models}})


def get_all_users(model):
    if model['title']==None:return
    (Media.objects.create(**model))


def export_view(req):
    return render(req, 'date-time-picker.html')


@csrf_exempt
def export_page(req):
    js=json.loads(req.POST['data'])
    print(js)
    js=js[0]
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    writer = csv.writer(response)
    writer.writerow([' ID', 'title', 'images', 'price', 'description', 'url'])
    writer.writerow([1,js.get('title'),js.get('images'),js.get('price'),js.get('description'),js.get("url")])
    # return HttpResponse(req.POST.dict()['data'])
    return response



def export(req):
    print(req.GET)
    from_date = datetime.fromtimestamp(int(req.GET['from'])/1000)
    to_date = datetime.fromtimestamp(int(req.GET['to'])/1000)
    print(from_date, to_date)
    q = Media.objects.filter(datetime__gte=from_date, datetime__lte=to_date)
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    writer = csv.writer(response)
    writer.writerow([' ID', 'title', 'images', 'price', 'description', 'url'])
    studs = q.values_list('id', 'title', 'images',
                          'price', 'description', 'url')
    for std in studs:
        writer.writerow(std)
    return response
