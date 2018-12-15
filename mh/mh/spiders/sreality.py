import json

import scrapy

from .sreality_create_url import create_url

"""
required:
pages: number of pages to scrape

1st option 
spec: copy the complete API URL with search details (firefox -> search -> ctrl-shift-e -> copy the first XHR)


2nd option for all but projects - main and ctype argument required
main: 1 - byty, 2 - domy, 3 - pozemky, 4 - komercni, 5 - ostatni
ctype: 1 - prodej, 2 - pronajem, 3 - drazba
area: 10 - praha, 11 - stredocesky_kraj and so on

example: https://www.sreality.cz/api/cs/v2/estates?category_main_cb=2&category_type_cb=1&per_page=60
&locality_region_id=10|11
=> domy, prodej, 60 zaznamu na strance, Praha + Stredocesky kraj

TODO: example: https://www.sreality.cz/api/cs/v2/projects?per_page=60

When converting the .csv file to an excel sheet, set the 'telefono' column to 'text' type! 
"""


class SrealitySpider(scrapy.Spider):
    name = 'sreality'

    def start_requests(self):
        """Create a list of API URLs of pages with results based on attributes and send them to parse."""

        # TODO: find a way of finding the API URL automatically
        pages = getattr(self, 'pages', 1)
        spec = getattr(self, 'spec', None)

        per_page = 60
        main = getattr(self, 'main', 1)
        ctype = getattr(self, 'ctype', 1)
        area = getattr(self, 'area', None)

        if spec:
            urls = [f'{spec}&page={page}' for page in range(1, int(pages) + 1)]
        else:
            full_area = ''
            if area:
                full_area = '&locality_region_id=' + area

            urls = [f'https://www.sreality.cz/api/cs/v2/estates?' \
                    f'category_main_cb={main}&category_type_cb={ctype}&per_page={per_page}&page={page}{full_area}'
                    for page in range(1, int(pages) + 1)]

        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """Get all children API URLs of every ad in the result page and send to parse.

        :param response: Response object of an API with results.
        """

        json_response = json.loads(response.body)

        try:
            links = [json_response['_embedded']['estates'][number]['_links']['self']['href']
                     for number in range(len(json_response['_embedded']['estates']))]
        except KeyError:
            links = [json_response['projects'][ad]['_links']['self']['href']
                     for ad in range(len(json_response['projects']))]

        for link in links:
            yield response.follow(f'https://www.sreality.cz/api{link}', self.parse_offer)

    @staticmethod
    def parse_offer(response):
        """Get all required fields from an API of an ad and send to the output.

        :param response: Response object of an API of an ad.
        """

        json_response = json.loads(response.body)

        try:
            title = f"{json_response['name']['value']}, {json_response['locality']['value']}"
        except KeyError:
            title = f"{json_response['project_name']}, {json_response['full_address']}"

        try:
            seller = json_response['_embedded']['seller']['user_name']
        except KeyError:
            try:
                seller = json_response['contact']['name']
            except KeyError:
                try:
                    seller = json_response['_embedded']['rk']['name']
                except KeyError:
                    seller = ''

        try:
            phone1 = json_response['_embedded']['seller']['phones'][0]['number']
            code1 = json_response['_embedded']['seller']['phones'][0]['code']
        except (IndexError, KeyError):
            try:
                phone1 = json_response['contact']['phones'][0]['number']
                code1 = json_response['contact']['phones'][0]['code']
            except (IndexError, KeyError):
                try:
                    phone1 = json_response['_embedded']['rk']['phones'][0]['number']
                    code1 = json_response['_embedded']['rk']['phones'][0]['code']
                except (IndexError, KeyError):
                    phone1 = ''
                    code1 = ''
        try:
            phone2 = json_response['_embedded']['seller']['phones'][1]['number']
            code2 = json_response['_embedded']['seller']['phones'][1]['code']
        except (IndexError, KeyError):
            try:
                phone2 = json_response['contact']['phones'][1]['number']
                code2 = json_response['contact']['phones'][1]['code']
            except (IndexError, KeyError):
                phone2 = ''
                code2 = ''

        if code1 != '':
            code1 = f'+{code1} '
        if code2 != '':
            code2 = f'+{code2} '

        if phone2 != '' and phone2 != phone1:
            phones = f'{code1}{phone1[0:3]} {phone1[3:6]} {phone1[6:10]}, ' \
                     f'{code2}{phone2[0:3]} {phone2[3:6]} {phone2[6:10]}'
        else:
            phones = f'{code1}{phone1[0:3]} {phone1[3:6]} {phone1[6:10]}'

        try:
            email = json_response['_embedded']['seller']['email']
        except KeyError:
            try:
                email = json_response['contact']['email']
            except KeyError:
                try:
                    email = json_response['_embedded']['rk']['email']
                except KeyError:
                    email = ''

        # email seems to be always present
        yield {'titulo': title.strip(), 'contacto': seller.strip(), 'telefono': phones.strip(), 'email': email.strip(),
               'url': create_url(json_response)}
