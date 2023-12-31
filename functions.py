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


def lowercase_first(word: str) -> str:
    if not word:
        return ""

    return word[0].lower() + word[1:]


def uppercase_first(word: str) -> str:
    if not word:
        return ""

    return word[0].upper() + word[1:]


def load_keywords(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error while loading keywords from {filename}.")
        return []


def clean_url(url):
    # only for the results/urls dump
    for pattern in ["http://", "https://", "www."]:
        url = url.replace(pattern, "")
    return url.replace("/", "_").replace(".", "_")


def dump_results(results, output_directory, input_url):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    filename = os.path.join(output_directory, clean_url(input_url) + ".json")

    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)


def dump_urls(wanted_urls, output_directory, input_url):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    filename = os.path.join(output_directory, clean_url(input_url) + "_wanted.json")

    with open(filename, 'w') as json_file:
        json.dump(wanted_urls, json_file, indent=4)