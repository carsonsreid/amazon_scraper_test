import requests
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/111.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def get_search_results(keyword):
    logging.info(f"Searching Amazon for keyword: '{keyword}'")
    query = keyword.replace(' ', '+')
    url = f"https://www.amazon.com/s?k={query}"
    logging.info(f"Constructed URL: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []

    if response.status_code != 200:
        logging.error(f"Failed to fetch search page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('div', {'data-component-type': 's-search-result'})
    logging.info(f"Found {len(listings)} search results.")

    results = []
    for item in listings:
        try:
            title_elem = item.h2
            if title_elem:
                title = title_elem.text.strip()
                link = title_elem.a['href']
                full_url = f"https://www.amazon.com{link}"
                results.append(full_url)
                logging.debug(f"Found product: {title} | URL: {full_url}")
        except Exception as e:
            logging.warning(f"Failed to parse a result block: {e}")

    return results
