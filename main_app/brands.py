from main_app.models import Media

class Brands():
    def __init__(self, data, url: str):
        self.url = url
        self.data = data

    def start(self):
        url = self.url
        if url.startswith('https://www.trendyol.com'):
            return self.trendyol()
        elif url.startswith('https://www.zara.com'):
            return self.zara()
        elif url.startswith('https://shop.mango.com'):
            return self.mango()
        elif url.startswith('https://www.pullandbear.com/'):
            return self.pullandbear()
        elif url.startswith('https://www2.hm.com'):
            return self.hm()
        elif url.startswith('https://www.lcwaikiki.com'):
            return self.lcwaikiki()
        elif url.startswith("https://www.thebodyshop.com.tr"):
            return self.body_shop()
        elif url.startswith('https://www.watsons.com.tr/'):
            return self.watsons()

    def trendyol(self):
        pass

    def zara(self):
        main_content = self.data.css('div.product-detail-view__main')
        images = (main_content.css("img::attr(src)").extract())
        price = (main_content.css('span.price-current__amount::text').extract())
        title = (main_content.css('span.structured-component-text span::text').extract())
        m = Media.objects.create(images=images, price=price, title=title)
        return m

    def mango(self):
        main_content = self.data.css('main.product-detail')
        print(main_content.css('span.product-sale::text').extract())
        for i in main_content.css('div.product-images img::attr(src)').extract():
            print("https:" + i)
        print(main_content.css("h1.product-name::text").extract())

    def pullandbear(self):
        pass

    def hm(self):
        main_content = self.data.css('#main-content div.product.parbase div.layout')
        for i in main_content.css('div.module.product-description.sticky-wrapper > '
                                  'figure img::attr('
                                  'src)').extract():
            print('https:' + i)
        print(main_content.css("#product-price > div span::text").extract())
        print(main_content.css("div.module.product-description.sticky-wrapper > "
                               "div.sub-content.product-detail-info.product-detail-meta.inner.sticky-on-scroll.semi"
                               "-sticky > div > section > h1::text").extract())

    def lcwaikiki(self):
        x = self.data
        print(x.css("#rightInfoBar > div:nth-child(1) > div > div:nth-child(3) > div > div > div > "
                    "span.price::text").extract())
        print(x.css("#rightInfoBar > div:nth-child(1) > div > div.row.title-info > div.col-xs-7.col-sm-9 > "
                    "div.product-title::text").extract())
        print(x.css("#productSliderPhotos > div.product-images-desktop.hidden-xs img::attr(src)").extract())

    def body_shop(self):
        x = self.data
        print(x.css('#fiyat2 > span.spanFiyat::text').extract())  # price
        for i in x.css('#imgurunresmi::attr(src)').extract():
            print('https://www.thebodyshop.com.tr/' + i)
        print(x.css("#ProductDetailMain > div > div.RightDetail.varyantYok > div.TopList > div.ProductName > h1 > "
                    "span::text").extract())  # title
        print(x.css("#tbsTab1::text").extract())  # description


def watsons(self):
    x = self.data
    print(x.css('#prodDetailRight > ul').extract())
    print(x.css("#prodDetailRight > div.product-detail-right.z-1 > div > h1::text").extract())
    print(x.css("#detailSlider > div.owl-stage-outer > div > div.owl-item.active > div > img::attr(src)").extract())
