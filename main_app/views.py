from concurrent.futures import thread
import threading
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from playwright.sync_api import sync_playwright
from scrapy import Selector
import main_app.brands
from main_app.models import Media
from asgiref.sync import sync_to_async
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
    p=''
    models=[]
    for i in data:
        i: str
        with sync_playwright() as playwright:
            browser =  playwright.webkit.launch()
            context =  browser.new_context()
            page =  context.new_page()
            page.goto(i, timeout=120 * 1000)
            p = (page.inner_html('html'))
            
            x= Selector(text=p)
            # print(p)
            b = main_app.brands.Brands(x, i)
            model = ( b.start())
            models+=model
            
            print(model)
            print("started " + i)
            x = threading.Thread(target=get_all_users, args=(model,))  
            x.start()
    return render(req,"insert_data_page.html",{"models":models})

def get_all_users(model):
    ( Media.objects.create(**model))