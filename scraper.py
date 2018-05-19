"""
Hier eintragen!
"""
import urllib.request
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.raw_data = {}
        self.standardized_data = {}


class MobileScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.list_top_level_categories = []
        self.top_level_category_urls = {"lkw_ueber_7.5t": "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=ALSO_DAMAGE_UNREPAIRED&grossPrice=false&isSearchRequest=true&maxPowerAsArray=PS&minPowerAsArray=PS&scopeId=TO75", "sattelzugmaschinen": "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=ALSO_DAMAGE_UNREPAIRED&grossPrice=false&isSearchRequest=true&maxPowerAsArray=PS&minPowerAsArray=PS&scopeId=STT"}

    def fetch_raw_data(self):
        for category in self.top_level_category_urls:
            self.list_top_level_categories.append(MobileTopLevelCategory(category, self.top_level_category_urls[category]))

        for category in self.list_top_level_categories:
            category.request_html_code()


class MobileTopLevelCategory:
    def __init__(self, category_name: str, url: str):
        self.category_name = category_name
        self.url = url
        self.html_code = ""

    def request_html_code(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
            handler = urllib.request.urlopen(req)

        except urllib.request.HTTPError as e:
            raise ConnectionError(str(e))
        except urllib.request.URLError as e:
            raise ConnectionError("The server to : " + self.url + " could not be found!")

        else:
            self.html_code = handler.read()