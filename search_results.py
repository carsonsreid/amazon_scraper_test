import request
from bs4 import BeautifulSoup
import loggin

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/111.0.0.0 Safari/537.36"
    )
}

def get_search_results(keyword: str) -> list:
    loggin.debug(f"Searching Amazon for keyword: '{keyword}'")
    query = keyword.replace(' ', '+')
    url = f"https://www.amazon.com/s?k={query}"
    loggin.debug(f"Constructed URL: {url}")

    try:
        response = request.get(url, headers=HEADERS)
    except:
        return None

    if response.status_code != 200:
        loggin.error(f"Status code: {response.status}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('div', {'data-component-type': 's-search-result'})
    loggin.debug(f"Found {len(listings)} result blocks.")

    urls = []
    for block in listings:
        try:
            title_elem = block.find("h2")
            link = title_elem.a['href']
            full_url = "https://amazon.com" + link
urls.append(full_url)
            loggin.debug(f"{title_elem.text.strip()} | {full_url}")
        except:
            continue

    return urls
