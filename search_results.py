import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/111.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def get_search_results(search_term):
    search_query = search_term.replace(' ', '+')
    url = f"https://www.amazon.com/s?k={search_query}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch search results: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    product_urls = []

    for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
        link_tag = item.find('a', {'class': 'a-link-normal s-no-outline'})
        if link_tag and 'href' in link_tag.attrs:
            product_url = "https://www.amazon.com" + link_tag['href']
            product_urls.append(product_url)

    return product_urls
