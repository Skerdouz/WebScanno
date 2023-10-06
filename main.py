import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse, urlunparse


class StopSearch(Exception):
    pass


# normalise by adding / at the end
def normalize_url(url):
    parts = list(urlparse(url))
    if not parts[2].endswith('/'):
        parts[2] += '/'
    return urlunparse(parts)



# main function
def search_policies(url, keywords, max_depth, stop_flag, visited_urls):
    try:
        if max_depth <= 0 or stop_flag[0]:
            return

        url = normalize_url(url)
        # mark url as already visited
        visited_urls.add(url)

        response = requests.get(url)
        content = response.text

        # get if cookies/cookie banner exist
        cookies_exist = 'set-cookie' in response.headers
        cookie_banner_exist = 'cookie' in content.lower()

        cookie_info = "yes" if cookies_exist else "no"
        banner_info = "yes" if cookie_banner_exist else "no"

        # print infos in the console
        print(f"URL: {url}")
        print(f"Cookies: {'✅' if cookies_exist else '❌'}")
        print(f"Cookie Banner: {'✅' if cookie_banner_exist else '❌'}")

        # go through all keywords
        for keyword in keywords:
            if re.search(keyword, content, re.IGNORECASE):
                # if keyword found, print info & write in result.json
                print(f"!!Keyword '{keyword}: ✅")
                # stop_flag[0] = True
                results.setdefault(url, {"Cookies": cookie_info, "Cookie banner": banner_info,
                                         "Keywords": []})["Keywords"].append(keyword)

        soup = BeautifulSoup(content, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # go through found links on actual url, check if they are related and then proceed to build the url
        for link in links:
            if link.startswith('/') or url in link:
                if link.startswith('/'):
                    link = urljoin(url, link)
                if normalize_url(link) not in visited_urls:
                    search_policies(link, keywords, max_depth - 1, stop_flag, visited_urls)

    except Exception as e:
        print(f"Error on {url}: {str(e)}")


with open('keywords.json', 'r') as json_file:
    data = json.load(json_file)
    keywords_to_search = data.get('keywords', [])

url = "https://certi-data.fr"
max_depth = 3

stop_flag = [False]
visited_urls = set()

results = {}


search_policies(url, keywords_to_search, max_depth, stop_flag, visited_urls)

# if results, then proceed to write in results.json
if results:
    with open('results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)