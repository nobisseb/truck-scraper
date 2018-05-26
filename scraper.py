"""
Hier eintragen!
"""
from bs4 import BeautifulSoup
import html_request
import re
import unicodedata

class Scraper:
    def __init__(self):
        # raw data to be standardized before storage in a database
        self.raw_data = {}
        # standardized data ready to be stored in a database
        self.standardized_data = {}


class Item:
    def __init__(self, url: str):
        self.url = url
        self.html = ""
        self.raw_data = self.extract_raw_data_from_mobile_url(self.url)

    def extract_raw_data_from_mobile_url(self, url):
        html = html_request.request_html_code(url)
        raw_data = {'technische_daten': {}, 'title': ""}

        soup = BeautifulSoup(html, 'html.parser')

        raw_data_technische_daten = self.extract_technische_daten_from_html(soup)
        raw_data["technische_daten"].update(raw_data_technische_daten)

        raw_title = self.extract_title_from_html(soup)
        raw_data.update({'title': raw_title})

        raw_net_price = self.extract_net_price_from_html(soup)
        raw_data.update({'net_price': raw_net_price})
        print(raw_data)
        return raw_data

    def extract_technische_daten_from_html(self, soup):
        raw_data_technische_daten = {}
        # search the raw html for category/value pairs in "Technische Daten" section
        for raw_category in soup.find_all('div', {'class': 'g-row u-margin-bottom-9'}):
            soup_cat = BeautifulSoup(str(raw_category), 'html.parser')

            # extract every category
            category = str(soup_cat.strong)[8:-9]
            # extract the corresponding value
            value = re.findall("-v\">.*</div></div>$", str(raw_category))[0][4:-12]

            # normalize the unicode strings for category and value
            category_uni = unicodedata.normalize("NFKD", category)
            value_uni = unicodedata.normalize("NFKD", value)

            raw_data_technische_daten.update({category_uni: value_uni})

        return raw_data_technische_daten

    def extract_title_from_html(self, soup):
        # extract the item title from html
        raw_data_title = soup.find('h1', {'class': 'h2', 'id': 'rbt-ad-title'})
        raw_data_title = raw_data_title.string

        return raw_data_title

    def extract_net_price_from_html(self, soup):
        # extract the item netto price from html
        raw_data_net_price = soup.find('span', {'class': 'h3 rbt-prime-price'})
        raw_data_net_price = str(raw_data_net_price)[33:-20]

        return raw_data_net_price


class MobileScraper(Scraper):
    def __init__(self):
        super().__init__()
        # a list which stores instances the mobile toplevel category class
        self.list_top_level_categories = []
        # mobile top-level categories to be handled
        self.top_level_category_urls = {"lkw_ueber_7.5t": "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=ALSO_DAMAGE_UNREPAIRED&grossPrice=false&isSearchRequest=true&scopeId=TO75", "sattelzugmaschinen": "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=ALSO_DAMAGE_UNREPAIRED&grossPrice=false&isSearchRequest=true&scopeId=STT"}

    def fetch_raw_data(self):
        # for every top-level category create a MobileTopLevelCategory instance and store it in a list
        for category in self.top_level_category_urls:
            self.list_top_level_categories.append(MobileTopLevelCategory(category, self.top_level_category_urls[category]))


class MobileTopLevelCategory:
    def __init__(self, category_name: str, category_url: str):
        # name of the mobile search category
        self.category_name = category_name
        # basic category search url -> &pageNumber=2
        self.category_url = category_url
        # urls to all 50 search pages
        self.urls_all_search_pages = self.construct_search_pages_urls(self.category_url)
        # request the html code for all search page urls
        self.htmls_all_search_pages = html_request.request_html_code_from_list_of_urls(self.urls_all_search_pages)
        # urls to every truck
        self.urls_all_items = self.extract_all_item_urls(self.htmls_all_search_pages)
        # construct a list of item objects
        self.items = self.construct_item_objects(self.urls_all_items)
        for item in self.items:
            print(item.raw_data)

    def construct_search_pages_urls(self, category_url: str):
        list_urls = []
        list_1_to_50 = list(range(1, 5))

        # for pages 1 to 50 construct a url to access the search result pages
        for x in list_1_to_50:
            list_urls.append(category_url + "&pageNumber=" + str(x))

        return list_urls

    def extract_all_item_urls(self, list_htmls_search_pages):
        urls_all_items = []

        for html_code in list_htmls_search_pages:
            list_item_urls = self.extract_item_urls_from_html(html_code)
            urls_all_items += list_item_urls

        return urls_all_items

    def extract_item_urls_from_html(self, html_code):
        list_urls = []

        soup = BeautifulSoup(html_code, 'html.parser')

        for link in soup.find_all('a', {'class': 'link--muted no--text--decoration result-item'}):
            span_tag_content_href = link.get('href')
            list_urls.append(span_tag_content_href)

        return list_urls

    def construct_item_objects(self, list_item_urls):
        list_item_objects = []

        for url in list_item_urls:
            list_item_objects.append(Item(url))

        return list_item_objects
