import scrapy
import re

phone_regex = re.compile(r'(\+?(00)?\d{3})? ?-?\.?\d{2,3} ?-?\.?\d{2,3} ?-?\.?\d{2,3}( ?-?\.?\d{2,3})?')
email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')


def clean_phone(matches: list) -> str:
    cleaned_matches = [[char for char in match if char.isdigit() or char == '+'] for match in matches]
    phone_numbers = [match for match in cleaned_matches if len(match) >= 9]

    for phone_number in phone_numbers:
        phone_number.insert(-3, ' ')
        phone_number.insert(-7, ' ')
        phone_number.insert(-11, ' ')

    phone_numbers_cleaned = ', '.join(set([''.join(phone_number).strip() for phone_number in phone_numbers]))
    return phone_numbers_cleaned


class BezRealitkySpider(scrapy.Spider):
    name = "bezrealitky"

    def start_requests(self):
        url = 'https://www.bezrealitky.cz/vypis/'
        spec = getattr(self, 'spec', 'nabidka-prodej/byt/praha')
        yield scrapy.Request(f'{url}{spec}', self.parse)

    def parse(self, response):
        # follow links to individual rental offers
        for href in response.xpath('//a[@class="btn btn-shadow btn-primary btn-sm"]/@href').extract():
            yield response.follow(href, self.parse_offer)

        # follow pagination links
        for href in response.xpath('//a[@rel="next"]/@href').extract():
            yield response.follow(href, callback=self.parse)

    def parse_offer(self, response):

        def search_info_box(field):
            return response.xpath('//div[@class="col col-12 col-md-4 col-print-12 mt-minus d-none d-md-block"]'
                                  f'//div[text()="{field}"]/following-sibling::div[1]/text()').extract_first()

        def search_desc(field):
            desc_string = ' '.join(response.xpath('//p[@class="b-desc__info"]/text()').extract())

            if field == 'Telefon':
                m_phones = [x.group() for x in re.finditer(phone_regex, desc_string)]
                if m_phones:
                    return clean_phone(m_phones)
            elif field == 'E-mail':
                m_email = email_regex.search(desc_string)
                if m_email:
                    return m_email.group().strip()

        seller = search_info_box('Majitel')
        if not seller:
            seller = search_desc('Majitel')

        phone = search_info_box('Telefon')
        if not phone:
            phone = search_desc('Telefon')

        email = search_info_box('E-mail')
        if not email:
            email = search_desc('E-mail')

        title = response.xpath('//h1[@class="heading__title"]/text()').extract_first() + \
                response.xpath('//p[@class="heading__perex font-weight-medium"]/text()').extract_first().strip()

        if phone or email:
            yield {'titulo': title, 'contacto': seller, 'telefono': phone, 'email': email, 'url': response.url}

        # desc_string = ' '.join(response.xpath('//p[@class="b-desc__info"]/text()').extract())
        # yield {'text': desc_string}
