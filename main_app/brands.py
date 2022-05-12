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
        elif url.startswith('https://www.flo.com.tr/'):
            return self.flo()

    def trendyol(self):
        pass

    def zara(self):
        main_content = self.data
        print(200 * '&')
        model = {
            'images': filter(lambda x: not x.endswith('transparent-background.png'),
                             main_content.css("img.media-image__image.media__wrapper--media::attr(src)").extract()),
            'price': (main_content.css(
                '#main > article > div.product-detail-view__main > div.product-detail-view__side-bar > div.product-detail-info > div.product-detail-info__price > div > span > span > span::text').extract()[
                0]),
            'title': (main_content.css('h1.product-detail-info__header-name::text').extract()[0]),
            'description': main_content.css("div.expandable-text__inner-content p::text").extract()[0],
            'url': self.url
        }

        return model

    def mango(self):
        main_content = self.data.css('main.product-detail')
        model = {
            'price': (main_content.css('span.product-sale::text').extract()[0]),
            'images': list(
                map(lambda x: "https:" + x, main_content.css('div.product-images img::attr(src)').extract())),
            'title': (main_content.css("h1.product-name::text").extract()[0]),
            'url': self.url
        }
        return model

    def pullandbear(self):
        pass

    def hm(self):
        main_content = self.data.css('#main-content div.product.parbase div.layout')
        model = {
            'images': list(
                map(lambda x: 'https:' + x, main_content.css('div.module.product-description.sticky-wrapper > '
                                                             'figure img::attr('
                                                             'src)').extract()))
            ,
            "price": (main_content.css("#product-price > div span::text").extract()),
            'title': (main_content.css("div.module.product-description.sticky-wrapper > "
                                       "div.sub-content.product-detail-info.product-detail-meta.inner.sticky-on-scroll.semi"
                                       "-sticky > div > section > h1::text").extract()),
            'url': self.url
        }
        return model

    def lcwaikiki(self):
        x = self.data
        model = {
            'price': (x.css("#rightInfoBar > div:nth-child(1) > div > div:nth-child(3) > div > div > div > "
                            "span.price::text").extract()[0]),
            'title': (x.css("#rightInfoBar > div:nth-child(1) > div > div.row.title-info > div.col-xs-7.col-sm-9 > "
                            "div.product-title::text").extract()[0]),
            'images': (x.css("#productSliderPhotos > div.product-images-desktop.hidden-xs img::attr(src)").extract()),
            'url': self.url
        }
        return model

    def body_shop(self):
        x = self.data
        model = {
            'price': x.css('#fiyat2 > span.spanFiyat::text').get(),
            'title':
                x.css("#ProductDetailMain > div > div.RightDetail.varyantYok > div.TopList > div.ProductName > h1 > "
                      "span::text").get(),
            'description': x.css("#tbsTab1::text").get(),
            'images': list(
                map(lambda x: 'https://www.thebodyshop.com.tr/' + x, x.css('#imgurunresmi::attr(src)').extract())),
            'url': self.url
        }
        return model

    def watsons(self):
        x = self.data
        model = {'price': (x.css('#prodDetailRight span.detail-price::text').get()),
                 'title': (x.css("#prodDetailRight > div.product-detail-right.z-1 > div > h1::text").get()),
                 'images': (x.css(
                     "#detailSlider > div.owl-stage-outer > div > div.owl-item.active > div > img::attr(src)").extract()),
                 'url': self.url
                 }
        return model

    def flo(self):
        x = self.data
        model = {
            "title": x.css('h1.product__name.description.text-capital.order-1.js-product-name::text').get().replace(
                '\n', '').replace('   ', ''),
            "price": x.css("div.product__prices span.product__prices-sale::text").get(),
            "images": list(map(lambda i: i.split('url')[1].split('(')[1].split(')')[0].replace('"', ''),
                               x.css("div.zoomWindow::attr(style)").extract()))
        }
        return model

    def koton(self):

        x = self.data
        model = {
            "title": x.css("#content > div:nth-child(4) > div > div.col-xs-3.detailDescriptionContainer > div > "
                           "h1::text").get(),
            "price": x.css("#content div.price span::text").get(),
            "images": x.css('a.zoomImgLink img::attr(src)').extract()
        }
        return model
