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

    def fetch_raw_data(self):
        top_level_category_urls = {"lkw_ueber_7.5t": "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=ALSO_DAMAGE_UNREPAIRED&grossPrice=false&isSearchRequest=true&maxPowerAsArray=PS&minPowerAsArray=PS&scopeId=TO75", "sattelzugmaschinen": "https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=ALSO_DAMAGE_UNREPAIRED&grossPrice=false&isSearchRequest=true&maxPowerAsArray=PS&minPowerAsArray=PS&scopeId=STT"}

        for category in top_level_category_urls:
            try:
                url = top_level_category_urls[category]
            except urllib.URLError as e:
                print("The server to :" + url + "could not be found!")
            except urllib.HTTPError as e:
                print(e)
            else:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
                html_code = urllib.request.urlopen(req).read()
                print(html_code)