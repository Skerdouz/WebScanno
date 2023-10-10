# Web Keywords & Cookies Search Script

This Python script is designed to search for specific keywords (Privacy Policy by default) on a website by scanning its pages recursively up to a specified depth. It also checks for the presence of cookies and cookie consent banners on each page.

## Prerequisites

Before using the script, make sure you have the following dependencies installed:

- Python 3.x
- The following Python packages (install using `pip`):
  - `requests`
  - `beautifulsoup4`

You can install the required packages by running:

```bash
  pip install requests beautifulsoup4
```

## Usage

1. Clone this repository or Download the zip folder

2. Customize the `keywords.json` file with your desired keywords
```json
{
  "keywords": [
    "keyword1",
    "keyword2",
    "keyword3"
    ]
}
```

3. (Optional) Customize the wanted urls in `main.py` at line 63:
```python
if re.match(r'.*/(wanted_url_1|wanted_url_2|...)', link):
```

4. Run a terminal in the directory and run the script with the following format:
```bash
python main.py <str:url> <(optional)int:max_depth[default=3]>
example: python main.py https://www.certi-data.fr
```

## Output

After the script finished running, a `{url}.json` file will be created with all occurrences and cookies usage found,
and a `{url}_wanted.json` containing all the wanted urls found within the website.

`{url}.json` example:

```json
{
  "https://certi-data.fr/": {
    "Cookies": "no",
    "Cookie banner": "no",
    "Keywords": [
      "contact@"
    ]
  },
  "https://certi-data.fr/service-certi-data/": {
    "Cookies": "no",
    "Cookie banner": "yes",
    "Keywords": [
      "cookie",
      "cookies",
      "contact@",
      "droits"
    ]
  },
  "https://certi-data.fr/contact/": {
    [...]
  }
}
```
`{url}_wanted.json` example:
```json
{
    "URLS": [
        "https://certi-data.fr/contact/",
        "https://certi-data.fr/index.php/contact/"
    ]
}
```