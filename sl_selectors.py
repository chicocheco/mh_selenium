import time
import re

from selenium.common.exceptions import NoSuchElementException

email_regex = re.compile(r'[a-zA-Z0-9._%+-]+ ?@ ?[a-zA-Z0-9-]+ ?\. ?[a-zA-Z]{2,4}')


class TraumFerienWohnungen:

    def __init__(self, driver, first_listing_url, from_page, to_page):
        self.driver = driver
        self.first_listing_url = first_listing_url
        self.from_page = from_page
        self.to_page = to_page

    def setup_driver(self):
        self.driver.maximize_window()

    def get_number_last_page(self):
        self.setup_driver()
        return int(self.driver.find_element_by_xpath('//ul[@id="results-paginator"]/li[8]').text)

    def estate_urls(self):
        webelement_estate_urls = self.driver.find_elements_by_xpath('//a[@class="js-link"]')
        estate_urls = [webelement_estate_url.get_attribute('href') for webelement_estate_url in webelement_estate_urls]
        return estate_urls

    def create_add_listing_urls(self):
        # listings from page 2 and on have different URL pattern
        for page_num in range(self.from_page or 2, self.to_page + 1):
            url_chunks = self.first_listing_url.split('/')
            url_chunks[-2] = f'seite-{page_num}'
            yield (page_num, '/'.join(url_chunks))

    # these functions are run from direct_url
    def title(self):
        try:
            return self.driver.find_element_by_xpath('//span[@class="f-1 lh-initial bold fs-xxxxxl m-0 m--fs-m"]').text
        except NoSuchElementException:
            return ''

    def contact_name(self):
        try:
            return self.driver.find_element_by_xpath('//p[@class="fs-xl bold mb-s mt-s m--fs-m"]').text or 'Anonymous'
        except NoSuchElementException:
            return 'Anonymous'

    def open_phone_number_detail(self):
        try:
            self.driver.find_element_by_xpath('//a[@class="us-none fs-m df ai-c"]').click()
            # wait to open
            time.sleep(1)
            return True
        except NoSuchElementException:
            return False

    def list_phone_numbers(self):
        self.open_phone_number_detail()
        phone_numbers = []
        try:
            phone_numbers.append(self.driver.find_element_by_xpath('//li[@class="mb-s"]').text)
        except NoSuchElementException:
            pass
        try:
            phone_numbers.append(self.driver.find_elements_by_xpath('//li[@class="mb-s"]')[1].text)
        except IndexError:
            pass
        try:
            phone_numbers.append(self.driver.find_elements_by_xpath('//li[@class="mb-s"]')[2].text)
        except IndexError:
            pass
        if phone_numbers:
            return phone_numbers

    @staticmethod
    def list_emails():
        # this website don't provide email addresses
        return []


class MilAnuncios:

    phone_number_detail_opened = False

    def __init__(self, driver, first_listing_url, from_page, to_page):
        self.driver = driver
        self.first_listing_url = first_listing_url
        self.from_page = from_page
        self.to_page = to_page

    def setup_driver(self):
        self.driver.implicitly_wait(3)

    def get_number_last_page(self):
        self.setup_driver()
        return int(self.driver.find_element_by_xpath('//div[@class="adlist-paginator-summary"]').text.split(' ')[-1])

    def estate_urls(self):
        webelement_estate_urls = self.driver.find_elements_by_xpath('//a[@class="aditem-detail-title"]')
        estate_urls = [webelement_estate_url.get_attribute('href') for webelement_estate_url in webelement_estate_urls]
        return estate_urls

    def create_add_listing_urls(self):
        # listings from page 2 and on have different URL pattern
        for page_num in range(self.from_page or 2, self.to_page + 1):
            yield (page_num, self.first_listing_url + f'?pagina={page_num}')

    def title(self):
        try:
            return self.driver.find_element_by_xpath('//div[@class="pagAnuTituloBox"]/a').text
        except NoSuchElementException:
            return ''

    def list_emails(self):
        try:
            desc = self.driver.find_element_by_xpath('//p[@class="pagAnuCuerpoAnu"]').text
        except NoSuchElementException:
            desc = None
        if desc:
            # search() does not search for more than 1 match
            m_email = email_regex.search(desc)
        else:
            m_email = None
        if m_email:
            return [m_email.group().strip()]
        else:
            return []

    def open_phone_number_detail(self):
        # only clicking on the button does not work
        # TODO: consider a case of having the ID number of a different length
        estate_url = self.driver.current_url.split('/')[-1][-13:-4]
        phone_number_detail_url = \
            f'https://www.milanuncios.com/datos-contacto/?usePhoneProxy=0&from=detail&id={estate_url}'
        self.driver.get(phone_number_detail_url)
        self.phone_number_detail_opened = True

    # in popup
    def contact_name(self):
        if not self.phone_number_detail_opened:
            self.open_phone_number_detail()
        try:
            contact_name = self.driver.find_element_by_xpath('//strong').text
            if contact_name == '(Profesional)' or contact_name == '(Particular)':
                return 'Anonymous'
            elif '(Particular)' in contact_name:
                return contact_name[:-13]
            elif '(Profesional)' in contact_name:
                return contact_name[:-14]
            else:
                return contact_name
        except NoSuchElementException:
            return 'Anonymous'

    # in popup
    def list_phone_numbers(self):
        phone_numbers = []
        if not self.phone_number_detail_opened:
            self.open_phone_number_detail()
        try:
            phone_numbers.append(self.driver.find_element_by_xpath('//div[@class="telefonos"]').text)
        except NoSuchElementException:
            pass
        try:
            phone_numbers.append(self.driver.find_elements_by_xpath('//div[@class="telefonos"]')[1].text)
        except IndexError:
            pass
        # TODO: try to confirm, whether a third phone number can be found
        try:
            phone_numbers.append(self.driver.find_elements_by_xpath('//div[@class="telefonos"]')[2].text)
        except IndexError:
            pass
        if phone_numbers:
            return phone_numbers


class VivaWeek:

    def __init__(self, driver, first_listing_url, from_page, to_page):
        self.driver = driver
        self.first_listing_url = first_listing_url
        self.from_page = from_page
        self.to_page = to_page

    def setup_driver(self):
        self.driver.maximize_window()

    def get_number_last_page(self):
        self.setup_driver()
        return int(self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[7]').text)

    def estate_urls(self):
        webelement_estate_urls = self.driver.find_elements_by_xpath('//h2/a')
        estate_urls = [webelement_estate_url.get_attribute('href') for webelement_estate_url in webelement_estate_urls]
        return estate_urls

    def create_add_listing_urls(self):
        # listings from page 2 and on have different URL pattern
        for page_num in range(self.from_page or 2, self.to_page + 1):
            yield (page_num, self.first_listing_url + f'?page={page_num}')

    def title(self):
        try:
            return self.driver.find_element_by_xpath('//div[@class="col-md-10 titre-fiche content-titre"]/h1').text
        except NoSuchElementException:
            return ''

    def contact_name(self):
        try:
            # TODO: select the one which is True (not an empty string) using OR operator
            return self.driver.find_element_by_xpath('//span[@class="nom-proprio"]').text
        except NoSuchElementException:
            return 'Anonymous'

    def open_phone_number_detail(self):
        try:
            self.driver.find_element_by_xpath('//span[@class="btn btn-orange contact-email-btn"]').click()
            # wait to open
            time.sleep(1)
            return True
        except NoSuchElementException:
            return False

    def list_phone_numbers(self):
        phone_numbers = []
        if self.open_phone_number_detail():
            try:
                phone1 = self.driver.find_element_by_xpath('//div[@class="tel-number-data"]').text
                if 'De' in phone1:
                    phone_numbers.append(phone1[:-17])
                else:
                    phone_numbers.append(phone1)
            except NoSuchElementException:
                pass
            try:
                phone2 = self.driver.find_elements_by_xpath('//div[@class="tel-number-data"]')[1].text
                if 'De' in phone2:
                    phone_numbers.append(phone2[:-17])
                else:
                    phone_numbers.append(phone2)
            except IndexError:
                pass
            if phone_numbers:
                return phone_numbers
        else:
            return False

    @staticmethod
    def list_emails():
        # this website don't provide email addresses
        return []


class VacancesSeloger:

    def __init__(self, driver, first_listing_url, from_page, to_page):
        self.driver = driver
        self.first_listing_url = first_listing_url
        self.from_page = from_page
        self.to_page = to_page

    def setup_driver(self):
        # not able to open phone detail if mobile version of website not forced
        self.driver.set_window_size(600, 700)
        self.driver.set_window_position(0, 0)

    def get_number_last_page(self):
        self.setup_driver()
        return int(self.driver.find_element_by_xpath('//a[@class="pagination-chevron to-last-chevron"]')
                   .get_attribute('href').split('/')[-1])

    def estate_urls(self):
        webelement_estate_urls = self.driver.find_elements_by_xpath('//a[@class="vignette-link"]')
        estate_urls = [webelement_estate_url.get_attribute('href') for webelement_estate_url in webelement_estate_urls]
        return estate_urls

    def create_add_listing_urls(self):
        # listings from page 2 and on have different URL pattern
        for page_num in range(self.from_page or 2, self.to_page + 1):
            yield (page_num, self.first_listing_url + f'/{page_num}')

    def title(self):
        try:
            return self.driver.find_element_by_xpath('//h1[@itemprop="name"]').text
        except NoSuchElementException:
            return

    # TODO: if "Villes" was returned it means the IP address was blocked!
    def contact_name(self):
        try:
            # select the one which is not an empty string
            return self.driver.find_element_by_xpath('//p[@class="title"]').text or \
                   self.driver.find_elements_by_xpath('//p[@class="title"]')[1].text
        except NoSuchElementException:
            return 'Anonymous'

    def open_phone_number_detail(self):
        try:
            self.driver.find_element_by_xpath('//a[@class="jsInfosProfilTelPopin"]').click()
            # wait to open
            time.sleep(1)
            return True
        except NoSuchElementException:
            return False

    def list_phone_numbers(self):
        phone_numbers = []
        if self.open_phone_number_detail():
            try:
                phone_numbers.append(self.driver.find_element_by_xpath('//div[@class="tel-big"]').text)
            except NoSuchElementException:
                pass
            try:
                phone_numbers.append(self.driver.find_elements_by_xpath('//div[@class="tel-big"]')[1].text)
            except IndexError:
                pass
            if phone_numbers:
                return phone_numbers
        else:
            return False

    @staticmethod
    def list_emails():
        # this website don't provide email addresses
        return []


class Amivac(VacancesSeloger):
    # Amivac.com has the identical layout as VacSeloger.com now
    # TODO: leaving it as a child class in case of some differences
    def __init__(self, driver, first_listing_url, from_page, to_page):
        super().__init__(driver, first_listing_url, from_page, to_page)
        self.driver = driver
        self.first_listing_url = first_listing_url
        self.from_page = from_page
        self.to_page = to_page
