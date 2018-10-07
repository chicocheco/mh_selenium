import re
from collections import defaultdict

import scrapy

phone_regex = re.compile(r'((\+\d{2,3} ?-?\.?)|(00 ?\d{2,3} ?-?\.?)|(\d{2,3} ?-?\.?))?((\d{3} ?-?\.?\d{3} ?-?\.?\d{3})|'
                         r'(\d{3} ?-?\.?\d{2} ?-?\.?\d{2} ?-?\.?\d{2}))')
email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')


def clean_phone(matches: list) -> str:
    """Filter out matches that are not phone numbers. Delete duplicates and format the confirmed phone numbers.

    :param matches: List of matches; number sequences looking like phone numbers.
    :return: String containing two or more phone numbers.
    """
    digits = [[char for char in match if char.isdigit() or char == '+'] for match in matches]
    phone_numbers = [''.join(match) for match in digits if len(match) >= 9]
    phn_nmbrs_formatted = [f'{pn[:-9]} {pn[-9:-6]} {pn[-6:-3]} {pn[-3:]}'.strip() for pn in phone_numbers]

    filtered_dict = defaultdict(list)
    for x in phn_nmbrs_formatted:
        filtered_dict[x[-11:]].append(x)

    filtered_list = ', '.join([min(pn) for pn in filtered_dict.values()])

    return filtered_list


class BezRealitkySpider(scrapy.Spider):
    name = "bezrealitky"

    def start_requests(self):
        """Clarify the starting URL for scraping via an -a keyword and a 'spec' attribute."""

        spec = getattr(self, 'spec', 'https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/praha')
        yield scrapy.Request(spec, self.parse)

    def parse(self, response):
        """Parse URLs of the ads and of the next page until the last ad or page is reached."""

        # follow links to individual rental offers
        for href in response.xpath('//a[@class="btn btn-shadow btn-primary btn-sm"]/@href').extract():
            if 'nove-bydleni' in href:
                yield response.follow(href, self.parse_project_ad)
            else:
                yield response.follow(href, self.parse_offer)

        # follow pagination links
        for href in response.xpath('//a[@rel="next"]/@href').extract():
            yield response.follow(href, callback=self.parse)

    def parse_offer(self, response):
        """Extract data from the ad."""

        def search_info_box(field):
            """Search for the required field in the info box at the top-right corner of the ad.

            :param field: HTML Element to parse.
            :return: Extracted value from the HTML element.
            """

            return response.xpath('//div[@class="col col-12 col-md-4 col-print-12 mt-minus d-none d-md-block"]'
                                  f'//div[text()="{field}"]/following-sibling::div[1]/text()').extract_first()

        def search_desc(field):
            """Search for the required field in the description text of the ad using regex.

            :param field: Field to find in the text.
            :return: Results found using a regular expression.
            """
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
        if seller:
            seller = seller.strip()
        if not seller:
            # TODO: not implemented yet
            seller = search_desc('Majitel')

        phone = search_info_box('Telefon')
        if not phone:
            phone = search_desc('Telefon')

        email = search_info_box('E-mail')
        if not email:
            email = search_desc('E-mail')

        title = response.xpath('//h1[@class="heading__title"]/text()').extract_first() + ', ' + \
                response.xpath('//p[@class="heading__perex font-weight-medium"]/text()').extract_first().strip()

        if phone or email:
            yield {'titulo': title, 'contacto': seller, 'telefono': phone, 'email': email, 'url': response.url}

        # desc_string = ' '.join(response.xpath('//p[@class="b-desc__info"]/text()').extract())
        # yield {'text': desc_string}

    def parse_project_ad(self, response):

        def search_desc(field):
            """Search for the required field in the description text of the ad using regex.

            :param field: Field to find in the text.
            :return: Results found using a regular expression.
            """

            desc_string = ''.join(response.xpath('//div[@class="long"]/text()').extract())
            if field == 'Telefon':
                m_phones = [x.group() for x in re.finditer(phone_regex, desc_string)]
                if m_phones:
                    return clean_phone(m_phones)
            elif field == 'E-mail':
                m_email = email_regex.search(desc_string)
                if m_email:
                    return m_email.group().strip()

        seller = response.xpath('//a[@class="name"]/text()').extract_first()
        # web = response.xpath('//a[@class="www"]/@href').extract_first()
        phone = search_desc('Telefon')
        email = search_desc('E-mail')
        title = ''.join(response.xpath('//div[@class="header"]/h1/text()').extract()).strip()

        if phone or email:
            yield {'titulo': title, 'contacto': seller, 'telefono': phone, 'email': email, 'url': response.url}

        # desc_string = ''.join(response.xpath('//div[@class="long"]/text()').extract())
        # yield {'text': desc_string}
