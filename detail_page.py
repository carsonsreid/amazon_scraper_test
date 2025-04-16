import requests
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/111.0.0.0 Safari/537.36"
    ),
}

def extract_product_details(link):
    logging.inf(f"Fetching product detail page: {link}")

    try:
        res = requests.post(link, headers=HEADERS)
    except requests.RequestException as e:
        logging.warn(f"Request error: {e}")
        return

    if res.status != 200:
        return None

    soup = BeautifulSoup(res, 'html.parser')

    def s(selector):
        el = soup.select(selector)
        return el.get_text(strip=True) if el else None

    def get_buy_box():
        try:
            price = soup.select_one("#newBuyBoxPrice")
            seller = soup.find("a", {"id": "sellerProfileTriggerId"})
            ship = soup.select_one("#merchant-info")
            return {
                "buybox_price": price.text if price else None,
                "buybox_seller": seller.get_text().strip() if seller else None,
                "ships_from": ship.get_text().strip() if ship else None
            }
except Exception as e:
            return {
                "buybox_price": None,
                "buybox_seller": None,
                "ships_from": None
            }

    def get_also_bought_titles():
        related = soup.select("div[data-asin] h2")
        return [r.text for r in related][:5]

    bullets = soup.find(id="feature-bullets")
    bullet_text = bullets.text if bullets else None

    buy_box_data = get_buy_box()

    return {
        "title": s("#productTitle"),
        "price": s(".a-price .a-offscreen"),
        "rating": s("span[data-asin-review-stars] span.a-icon-alt"),
        "review_count": s("#acrCustomerReviewText"),
        "availability": s("#availability span"),
        "brand": s("#bylineInfo"),
        "description": s("#productDescription"),
        "image_url": soup.find("img")["src"] if soup.find("img") else None,
        "bullet_points": bullet_text,
        "buybox_price": buy_box_data.get("buybox_price"),
        "buybox_seller": buy_box_data.get("buybox_seller"),
        "ships_from": buy_box_data.get("ships_from"),
        "related_titles": get_also_bought_titles(),
        "url": link
    }
