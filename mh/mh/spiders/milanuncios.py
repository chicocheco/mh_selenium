import re
import random

import scrapy

phone_regex = re.compile(r'(%u003\d){9}')

# NOT WORKING, BLOCKED BY DISTIL NETWORKS !!!
class MilAnunciosSpider(scrapy.Spider):
    name = 'milanuncios'

    download_delay = random.randint(10, 15)

    def start_requests(self):
        spec = getattr(self, 'spec', 'https://www.milanuncios.com/alquiler-vacaciones-en-las_palmas/')
        yield scrapy.Request(spec, self.parse)

    def parse(self, response):

        # get offer links
        for href in response.xpath('//a[@class="aditem-detail-title"]/@href').extract():
            yield response.follow(href, self.parse_offer)


        # get next page link
        for href in response.xpath(
                '//div[@class="adlist-paginator-pagelink adlist-paginator-pageselected"]/a[text()="Siguiente"]/@href')\
                .extract():
            yield response.follow(href, callback=self.parse)

    def parse_offer(self, response):
        # self.log(response.request.headers['User-Agent'])

        title = response.xpath('//div[@class="pagAnuTituloBox"]/a/text()').extract_first()

        url = response.url

        # assuming the length of the id is always the same
        ad_id = url.split('/')[-1][-13:-4]

        seller_url = f'https://www.milanuncios.com/datos-contacto/?usePhoneProxy=0&from=detail&id={ad_id}'

        yield scrapy.Request(seller_url, self.parse_contact,
                             meta={'title': title, 'url': url}, dont_filter=True)

    @staticmethod
    def parse_contact(response):

        seller = response.xpath('//strong/text()').extract_first()

        lst_to_search = response.xpath('//script').extract()
        text_to_search = ''.join(lst_to_search)
        m_phones = [x.group() for x in re.finditer(phone_regex, text_to_search)]
        phone = ', '.join([num[5::6] for num in m_phones])

        email = ''

        yield {'titulo': response.meta['title'], 'contacto': seller, 'telefono': phone, 'email': email,
               'url': response.meta['url']}
