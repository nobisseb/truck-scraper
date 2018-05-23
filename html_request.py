import urllib.request
import time
import random


def request_html_code(url):
    # use a user agent to request the html code for a given url"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
        print("Requesting url: " + url)
        handler = urllib.request.urlopen(req)

        # sleep for a couple of seconds
        time.sleep(random.randint(1,3))

    # error handling if the request fails
    except urllib.request.HTTPError as e:
        raise ConnectionError(str(e))
    except urllib.request.URLError as e:
        raise ConnectionError("The server to : " + url + " could not be found!")

    # if the request is successful return the whole html of the url as a string
    else:
        html_code = handler.read()
        return html_code


def request_html_code_from_list_of_urls(list_urls: list):
    list_all_htmls = []

    # for every url in the list request a html code and return it to the list
    for url in list_urls:
        html_code = request_html_code(url)
        list_all_htmls.append(html_code)

    return list_all_htmls

