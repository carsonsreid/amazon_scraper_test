import logging
import time
import pandas as pd
from search_results import get_search_results
from detail_page import extract_product_details

# Configure logging
logging.basicConfig(
    filename='scraper.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
    filename='scraper.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    search_term = "Best Kids Toys"
    logging.info(f"Starting Amazon scrape for search term: '{search_term}'")

    try:
        product_urls = get_search_results(search_term)
        logging.info(f"Retrieved {len(product_urls)} product URLs from search results.")
    except Exception as e:
        logging.error("Failed during search results scraping", exc_info=True)
        return

    product_details = []
    for idx, url in enumerate(product_urls, 1):
        logging.info(f"[{idx}/{len(product_urls)}] Scraping detail page: {url}")
        try:
            details = extract_product_details(url)
            if details:
                product_details.append(details)
                logging.info(f"✔ Successfully scraped product: {details.get('title')}")
            else:
                logging.warning(f"✘ No data returned for: {url}")
        except Exception as e:
            logging.error(f"❌ Error scraping detail page: {url}", exc_info=True)
        time.sleep(2)

    df = pd.DataFrame(product_details)
    df.to_csv("amazon_products.csv", index=False)
    logging.info("✅ Scraping complete. Data saved to 'amazon_products.csv'.")

if __name__ == "__main__":
    main()
