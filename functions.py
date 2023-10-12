import json
import os
from urllib.parse import urlparse, urlunparse


def normalize_url(url):
    parts = list(urlparse(url))
    if not parts[2].endswith('/'):
        parts[2] += '/'
    if parts[1].startswith("www."):
        parts[1] = parts[1][4:]

    return urlunparse(parts)


def load_keywords(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data.get('keywords', [])


def dump_results(results, output_directory, input_url):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    filename = os.path.join(output_directory,
                            input_url.replace("http://", "").replace("https://", "").replace("www.", "").replace(
                                "/", "_").
                            replace(".", "_") + ".json")
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)


def dump_urls(wanted_urls, output_directory, input_url):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    filename = os.path.join(output_directory,
                            input_url.replace("http://", "").replace("https://", "").replace("www.", "").replace(
                                "/", "_").
                            replace(".", "_") + "_wanted.json")
    with open(filename, 'w') as json_file:
        json.dump(wanted_urls, json_file, indent=4)