from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from playwright.sync_api import sync_playwright
from scrapy import Selector
import main_app.brands


# Create your views here.
def main_page(req):
    return render(req, 'main_page.html')


def extract_data(url):
    with sync_playwright() as playwright:
        webkit = playwright.webkit
        browser = webkit.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, timeout=120 * 1000)
        p = (page.inner_html('html'))
        x=Selector(text=p)
        b = main_app.brands.Brands(x, url)
        model = b.start()
        return model
        print(model)
        print(100 * '&')
        print("started" + url)


def data_insert(req: WSGIRequest):
    a = dict(req.POST)
    data = []
    for i in a.keys():
        i = str(i)
        if i.startswith('data'):
            data += (a[i])
    print(data)
    for i in data:
        i: str
        extract_data(i)
    return HttpResponse("fsd")
