import scrapy


class RealityIdnesSpider(scrapy.Spider):
    name = 'reality_idnes'

    def start_requests(self):
        spec = getattr(self, 'spec', 'https://reality.idnes.cz/s/')
        yield scrapy.Request(spec, self.parse)

    def parse(self, response):
        for href in response.xpath('//a[@class="c-list-products__link"]/@href').extract():
            yield response.follow(href, self.parse_offer)
        for href in response.xpath('//a[@class="btn paging__next"]/@href').extract():
            yield response.follow(href, callback=self.parse)

    def parse_offer(self, response):
        title = response.xpath('//h1[@class="b-detail__title"]/span/text()').extract_first().strip()
        url = response.url

        seller_url = response.xpath('//h2[@class="b-author__title"]/a/@href').extract_first()
        yield scrapy.Request(seller_url, self.parse_seller_page, meta={'title': title, 'url': url})

    def parse_seller_page(self, response):
        try:
            seller = response.xpath('//h2[@class="b-author__title"]/text()').extract_first().strip()
            phone = response.xpath('//a[@class="item-icon item-icon--md measuring-data-layer"]/text()').extract()[-1]\
                .strip()
            email = response.xpath('//a[@class="item-icon item-icon--md"]/text()').extract()[-1].strip()
        except AttributeError:
            seller = response.xpath('//h1[@class="b-annot__title mb-5"]/text()').extract_first().strip()
            phone = response.xpath('//a[@class="item-icon measuring-data-layer"]/text()').extract()[-1].strip()
            email = response.xpath('//a[@class="item-icon"]/text()').extract()[-1].strip()

        yield {'titulo': response.meta['title'], 'contacto': seller, 'telefono': phone, 'email': email,
               'url': response.meta['url']}
