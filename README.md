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

1. Clone this repository

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

3. Modify the url variable in `main.py` to specify the website URL you want to scan

4. Set the max_depth variable (3 by default) to define the maximum depth for recursive scanning

4. Run a terminal in the directory and run the script with the following command:
```bash
python main.py
```

## Output

After the script finished running, a `results.json` file will be created with all occurrences and cookies usage found.

results.json example:

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