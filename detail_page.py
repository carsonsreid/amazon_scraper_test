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

def extract_product_details(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch product page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    def get_text(selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None

    title = get_text("#productTitle")
    price = get_text(".a-price .a-offscreen")
    rating = get_text("span[data-asin-review-stars] span.a-icon-alt")
    review_count = get_text("#acrCustomerReviewText")
    image_tag = soup.select_one("#imgTagWrapperId img")
    image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

    # Extract ASIN from the product details
    asin = None
    asin_element = soup.find("th", string="ASIN")
    if asin_element:
        asin_td = asin_element.find_next_sibling("td")
        if asin_td:
            asin = asin_td.get_text(strip=True)

    description = get_text("#productDescription")
    availability = get_text("#availability .a-declarative")

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "review_count": review_count,
        "image_url": image_url,
        "asin": asin,
        "description": description,
        "availability": availability,
        "url": url
    }
