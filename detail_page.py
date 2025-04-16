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

def extract_product_details(url):
    logging.info(f"Fetching product detail page: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
    except requests.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
        return None

    if response.status_code != 200:
        logging.error(f"Failed to load product page. Status: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    def safe_select(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    product = {
        "title": safe_select("#productTitle"),
        "price": safe_select(".a-price .a-offscreen"),
        "rating": safe_select("span[data-asin-review-stars] span.a-icon-alt"),
        "review_count": safe_select("#acrCustomerReviewText"),
        "availability": safe_select("#availability span"),
        "brand": safe_select("#bylineInfo"),
        "bullet_points": [
            li.get_text(strip=True) for li in soup.select("#feature-bullets ul li") if li
        ],
        "description": safe_select("#productDescription"),
        "image_url": (
            soup.select_one("#imgTagWrapperId img")['src']
            if soup.select_one("#imgTagWrapperId img") else None
        ),
        "url": url
    }

    logging.debug(f"Extracted product data: {product}")
    return product
