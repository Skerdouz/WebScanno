import re
import sys
from urllib.parse import urljoin

from functions import normalize_url, load_keywords, dump_results, dump_urls, lowercase_first, uppercase_first

import requests
from bs4 import BeautifulSoup


# main function
def search_policies(url, keywords, url_keywords, max_depth, stop_flag, visited_urls, wanted_urls):
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
            t_keyword = uppercase_first(keyword)
            if re.search(keyword, content, re.IGNORECASE):
                print(f"!!Keyword -> '{keyword}: ✅")
                results.setdefault(url, {"Cookies": cookie_info, "Cookie banner": banner_info,
                                         "Keywords": []})["Keywords"].append(t_keyword)
            t_keyword = lowercase_first(keyword)
            if re.search(keyword, content, re.IGNORECASE):
                print(f"!!Keyword -> '{keyword}: ✅")
                results.setdefault(url, {"Cookies": cookie_info, "Cookie banner": banner_info,
                                         "Keywords": []})["Keywords"].append(t_keyword)

        # go through found links on actual url, check if they are related and then proceed to build the url
        for link in links:
            if len(links) == 0:
                print("NO URLS FOUNDS")
                break
            if link.startswith('/') or url in link:
                if link.startswith('/'):
                    link = urljoin(url, link)
                if normalize_url(link) not in visited_urls:
                    search_policies(link, keywords, url_keywords, max_depth - 1, stop_flag, visited_urls, wanted_urls)

                    # check if url is a wanted url
                    if re.match(fr'.*/({url_keywords})', link):
                        wanted_urls.setdefault("URLS", []).append(link)

    except Exception as e:
        print(f"Error on {url}: {str(e)}")


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

    data = load_keywords('keywords.json')
    keywords = data['keywords']
    url_keywords = '|'.join(data['urls'])

    stop_flag = [False]
    visited_urls = set()
    output_directory = input_url.replace("http://", "").replace("https://", "")

    search_policies(input_url, keywords, url_keywords, max_depth, stop_flag, visited_urls, wanted_urls)

    if results:
        dump_results(results, output_directory, input_url)
    if wanted_urls:
        dump_urls(wanted_urls, output_directory, input_url)
