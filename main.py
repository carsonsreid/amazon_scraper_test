import search_results
import detail_page
import pandas as pd
import time

def main():
    search_term = "Best Kids Toys"
    print(f"Searching for: {search_term}")
    
    # Get product URLs from search results
    product_urls = search_results.get_search_results(search_term)
    print(f"Found {len(product_urls)} products.")
    
    # Extract details for each product
    product_details = []
    for idx, url in enumerate(product_urls, 1):
        print(f"Processing ({idx}/{len(product_urls)}): {url}")
        details = detail_page.extract_product_details(url)
        if details:
            product_details.append(details)
        time.sleep(2)  # Be polite and avoid hitting Amazon too hard
    
    # Save the data to a CSV file
    df = pd.DataFrame(product_details)
    df.to_csv("amazon_products.csv", index=False)
    print("Data saved to amazon_products.csv")

if __name__ == "__main__":
    main()
