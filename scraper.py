"""
Hier eintragen!
"""
import urllib.request
from bs4 import BeautifulSoup


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

        # request the html_code of each top level category
        for category in self.list_top_level_categories:
            category.request_html_code()


class MobileTopLevelCategory:
    def __init__(self, category_name: str, url: str):
        self.category_name = category_name
        self.url = url
        self.html_code = ""

    def request_html_code(self):
        # use a user agent to request the data of mobile top-level category such as "lkw_ueber_7.5t"
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
            handler = urllib.request.urlopen(req)

        # error handling if the request fails
        except urllib.request.HTTPError as e:
            raise ConnectionError(str(e))
        except urllib.request.URLError as e:
            raise ConnectionError("The server to : " + self.url + " could not be found!")

        # if the request is successful store the whole html of the top level category page as a string
        else:
            self.html_code = handler.read()
            print(self.html_code)