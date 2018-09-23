import scrapy
import json


class SrealitySpider(scrapy.Spider):
    name = 'sreality'

    def start_requests(self):
        pages = getattr(self, 'pages', 1)
        urls = [f'https://www.sreality.cz/api/cs/v2/estates?' \
                f'category_main_cb=1&category_type_cb=1&per_page=20&page={page}' for page in range(1, int(pages) + 1)]
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):

        json_response = json.loads(response.body)

        links = [json_response['_embedded']['estates'][number]['_links']['self']['href'] for number in range(20)]

        for link in links:
            yield response.follow(f'https://www.sreality.cz/api{link}', self.parse_offer)

    def parse_offer(self, response):

        json_response = json.loads(response.body)

        try:
            seller = json_response['_embedded']['seller']['user_name']
        except KeyError:
            try:
                seller = json_response['contact']['name']
            except KeyError:
                seller = '---'

        try:
            email = json_response['_embedded']['seller']['email']
        except KeyError:
            try:
                email = json_response['contact']['email']
            except KeyError:
                email = '---'
        try:
            phone = json_response['_embedded']['seller']['phones'][0]['number']
        except KeyError:
            try:
                phone = json_response['contact']['phones'][0]['number']
            except KeyError:
                phone = '---'

        title = json_response['meta_description']

        if phone or email != '---':
            yield {'titulo': title, 'contacto': seller, 'telefono': phone, 'email': email, 'url': response.url}
