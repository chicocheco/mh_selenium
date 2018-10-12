import scrapy


class RealityIdnesSpider(scrapy.Spider):
    name = 'reality_idnes'
    # download_delay = 1

    def start_requests(self):
        spec = getattr(self, 'spec', 'https://reality.idnes.cz/s/')
        yield scrapy.Request(spec, self.parse)

    def parse(self, response):
        for href in response.xpath('//a[@class="c-list-products__link"]/@href').extract():
            yield response.follow(href, self.parse_offer)
        for href in response.xpath('//a[@class="btn paging__next"]/@href').extract():
            yield response.follow(href, callback=self.parse)

    def parse_offer(self, response):
        try:
            title = response.xpath('//h1[@class="b-detail__title"]/span/text()').extract_first().strip()
        except AttributeError:
            title = response.xpath('//h1[@class="b-detail__title"]/text()').extract_first().strip()
        url = response.url
        seller_url = response.xpath('//h2[@class="b-author__title"]/a/@href').extract_first()
        if seller_url:
            # don't filter the duplicated requests
            yield scrapy.Request(seller_url, self.parse_contact,
                                 meta={'title': title, 'url': url}, dont_filter=True)
        else:
            ad_id = response.url.split('/')[-2]
            if 'projekt' in response.url:
                base_project_url = '/'.join(response.url.split('/')[:-1])
                contact_url = base_project_url + f'/?s-result-popupName=reaction' \
                                           f'&s-sc[0]={ad_id}&s-sc[set]=1&do=s-result-openPopup'
            else:
                contact_url = f'https://reality.idnes.cz/estate/?s-result-popupName=reaction' \
                            f'&s-et=flat&s-ot=sale&s-sc[0]={ad_id}&s-sc[set]=1&do=s-result-openPopup'
            yield scrapy.Request(contact_url, self.parse_contact,
                                 meta={'title': title, 'url': url, 'popup': True}, dont_filter=True)

    @staticmethod
    def parse_contact(response):
        rp = scrapy.Selector(response)
        if 'popup' in response.meta:
            seller = rp.xpath('//h2[@class="b-author__title b-author__title--sm"]/text()').extract_first().strip()
            phone = rp.xpath('//span[@class="item-icon"]/text()').extract()[1].strip()
            if 'Odeslat zprávu' in phone:
                phone = ''
            email = ''
        else:
            try:
                seller = rp.xpath('//h2[@class="b-author__title"]/text()').extract_first().strip()
            except AttributeError:
                seller = rp.xpath('//h1[@class="b-annot__title mb-5"]/text()').extract_first().strip()
            if seller.startswith('Name'):
                seller = seller[5:]

            try:
                phone = rp.xpath('//a[@class="item-icon item-icon--md measuring-data-layer"]/text()').extract()[-1].strip()
            except IndexError:
                try:
                    phone = rp.xpath('//a[@class="item-icon measuring-data-layer"]/text()').extract()[-1].strip()
                except IndexError:
                    phone = 'not-found'
            if len(phone) > 16:
                phone = phone[:4] + phone[8:]

            try:
                email = rp.xpath('//a[@class="item-icon item-icon--md"]/text()').extract()[-1].strip()
            except IndexError:
                try:
                    email = rp.xpath('//a[@class="item-icon"]/text()').extract()[-1].strip()
                except IndexError:
                    email = 'not-found'

        yield {'titulo': response.meta['title'], 'contacto': seller, 'telefono': phone, 'email': email,
                   'url': response.meta['url']}
