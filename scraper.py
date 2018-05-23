"""
Hier eintragen!
"""
from bs4 import BeautifulSoup
import html_request
import re


class Scraper:
    def __init__(self):
        # raw data to be standardized before storage in a database
        self.raw_data = {}
        # standardized data ready to be stored in a database
        self.standardized_data = {}


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

    def construct_search_pages_urls(self, category_url: str):
        list_urls = []
        list_1_to_50 = list(range(1, 51))

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
