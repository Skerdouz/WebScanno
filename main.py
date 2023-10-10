import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse, urlunparse
import sys


# normalize by adding / at the end
def normalize_url(url):
    parts = list(urlparse(url))
    if not parts[2].endswith('/'):
        parts[2] += '/'
    if parts[1].startswith("www."):
        parts[1] = parts[1][4:]

    return urlunparse(parts)


# main function
def search_policies(url, keywords, max_depth, stop_flag, visited_urls, wanted_urls):
    try:
        if max_depth <= 0 or stop_flag[0]:
            return

        url = normalize_url(url)
        # mark url as already visited
        visited_urls.add(url)

        response = requests.get(url)
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # get if cookies/cookie banner exist
        cookies_exist = 'set-cookie' in response.headers
        cookie_banner_exist = 'cookie' in content.lower()

        cookie_info = "yes" if cookies_exist else "no"
        banner_info = "yes" if cookie_banner_exist else "no"

        # print infos in terminal
        print("")
        print(f" ---URL n°{len(visited_urls)}---")
        print(f"URL: {url}")
        print(f"Cookies: {'✅' if cookies_exist else '❌'}")
        print(f"Cookie Banner: {'✅' if cookie_banner_exist else '❌'}")

        # go through all keywords
        for u_keyword in keywords:
            keyword = u_keyword.encode('latin1').decode('utf-8')
            if re.search(keyword, content, re.IGNORECASE):
                print(f"!!Keyword -> '{keyword}: ✅")
                results.setdefault(url, {"Cookies": cookie_info, "Cookie banner": banner_info,
                                         "Keywords": []})["Keywords"].append(keyword)

        # go through found links on actual url, check if they are related and then proceed to build the url
        for link in links:
            if len(links) == 0:
                print("NO URLS FOUNDS")
                break
            if link.startswith('/') or url in link:
                if link.startswith('/'):
                    link = urljoin(url, link)
                if normalize_url(link) not in visited_urls:
                    search_policies(link, keywords, max_depth - 1, stop_flag, visited_urls, wanted_urls)

                    # check if url is a wanted url
                    # edit wanted urls here: 'example.com/(url1|url2|...)'
                    if re.match(r'.*/(contact|contacts|policy|privacy|cgu|cgv|confidentiality|terms)', link):
                        wanted_urls.setdefault("URLS", []).append(link)

    except Exception as e:
        print(f"Error on {url}: {str(e)}")


def load_keywords(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data.get('keywords', [])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <URL> <max_depth>")
        sys.exit(1)

    input_url = sys.argv[1]
    if len(sys.argv) >= 3:
        max_depth = int(sys.argv[2])
    else:
        max_depth = 3

    results = {}
    wanted_urls = {}

    keywords_to_search = load_keywords('keywords.json')

    stop_flag = [False]
    visited_urls = set()

    search_policies(input_url, keywords_to_search, max_depth, stop_flag, visited_urls, wanted_urls)

    if results:
        filename = (input_url.replace("http://", "").replace("https://", "").replace("www.", "").replace("/", "_").
                    replace(".", "_") + ".json")
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=4, ensure_ascii=False)

    if wanted_urls:
        filename = (input_url.replace("http://", "").replace("https://", "").replace("www.", "").replace("/", "_").
                    replace(".", "_") + "_wanted.json")
        with open(filename, 'w') as json_file:
            json.dump(wanted_urls, json_file, indent=4)
