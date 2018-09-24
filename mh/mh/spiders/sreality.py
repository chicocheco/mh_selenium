import scrapy
import json

# e.g.: scrapy crawl sreality -a main=2 -a ctype=1 -a pages=10 -o sreality.csv

"""
main: 1 - byty, 2 - domy, 3 - pozemky, 4 - komercni, 5 - ostatni
ctype: 1 - prodej, 2 - pronajem, 3 - drazba
area: 10 - praha, 11 - stredocesky_kraj

example: https://www.sreality.cz/api/cs/v2/estates?category_main_cb=2&category_type_cb=1&per_page=60
&locality_region_id=10|11

=> domy, prodej, 60 zaznamu na strance, Praha + Stredocesky kraj

When converting the .csv file to an excel sheet, set the 'telefono' column to 'text' type! 
"""


# TODO: add functionality for 'pozemky', 'komercni' and 'ostatni'
def create_url(json_response):
    base = 'https://www.sreality.cz/detail'
    locality = '/' + json_response['seo']['locality']
    id_offer = '/' + json_response['_links']['self']['href'].split('/')[-1]
    title1 = json_response['name']['value']

    lst = title1.split()
    new_lst = []

    if lst[0] == 'Prodej':
        new_lst.insert(0, '/prodej')
    elif lst[0] == 'Pron\u00e1jem':
        new_lst.insert(0, '/pronajem')
    elif lst[0] == 'Dra\u017eba':
        new_lst.insert(0, '/drazby')

    if lst[1] == 'bytu':
        new_lst.insert(1, '/byt')
    elif lst[1] == 'rodinn\u00e9ho':
        new_lst.insert(2, '/rodinny')
    elif lst[1] == 'vily':
        new_lst.insert(2, '/vila')
        new_lst.insert(1, '/dum')
    elif lst[1] == 'chaty':
        new_lst.insert(1, '/dum/chata')
    elif lst[1] == 'chalupy':
        new_lst.insert(1, '/dum/chalupa')
    elif lst[1:4] == ['projektu', 'na', 'klíč']:
        new_lst.insert(1, '/dum/na-klic')
    elif lst[1:3] == ['zemědělské', 'usedlosti']:
        new_lst.insert(1, '/dum/zemedelska-usedlost')

    if lst[2] == 'domu':
        new_lst.insert(1, '/dum')
    elif lst[2] == 'atypick\u00e9':
        new_lst.insert(2, '/atypicky')
    elif lst[2] == '6 pokoj\u016f a v\u00edce':
        new_lst.insert(2, '/6-a-vice')

    rooms = ['1+kk', '1+1', '2+kk', '2+1', '3+kk', '3+1', '4+kk', '4+1', '5+kk', '5+1']
    if lst[2] in rooms:
        new_lst.insert(2, '/' + lst[2])

    new_lst_joined = ''.join(new_lst)

    return f'{base}{new_lst_joined}{locality}{id_offer}'


class SrealitySpider(scrapy.Spider):
    name = 'sreality'

    def start_requests(self):

        # TODO: add searching specifics like a room combination
        per_page = 60
        pages = getattr(self, 'pages', 1)
        main = getattr(self, 'main', 1)
        ctype = getattr(self, 'ctype', 1)
        area = getattr(self, 'area', '')

        full_area = ''
        if area != '':
            full_area = '&locality_region_id=' + area

        urls = [f'https://www.sreality.cz/api/cs/v2/estates?' \
                f'category_main_cb={main}&category_type_cb={ctype}&per_page={per_page}&page={page}{full_area}'
                for page in range(1, int(pages) + 1)]

        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):

        json_response = json.loads(response.body)

        # TODO: make the per_page variable an argument that can be received from the start_request function
        per_page = 60
        if json_response['result_size'] % per_page != 0:
            per_page = json_response['result_size'] % per_page

        links = [json_response['_embedded']['estates'][number]['_links']['self']['href'] for number in range(per_page)]

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
                email = ''

        try:
            phone1 = json_response['_embedded']['seller']['phones'][0]['number']
            code1 = json_response['_embedded']['seller']['phones'][0]['code']
        except KeyError:
            try:
                phone1 = json_response['contact']['phones'][0]['number']
                code1 = json_response['contact']['phones'][0]['code']
            except KeyError:
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

        if code1:
            code1 = f'+{code1} '
        phone1_formatted = f'{code1}{phone1[0:3]} {phone1[3:6]} {phone1[6:10]}'
        if code2 != '':
            code2 = f'+{code2} '
        if phone2 != '' and phone2 != phone1:
            phone2_formatted = f', {code2}{phone2[0:3]} {phone2[3:6]} {phone2[6:10]}'
            phones = phone1_formatted + phone2_formatted
        else:
            phones = phone1_formatted

        title1 = json_response['name']['value']
        title2 = json_response['locality']['value']
        title = title1 + ', ' + title2

        yield {'titulo': title, 'contacto': seller, 'telefono': phones, 'email': email,
               'url': create_url(json_response), 'api_url': response.url}
