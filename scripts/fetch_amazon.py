import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Amazon API keys
PAAPI_ACCESS_KEY = os.getenv("PAAPI_ACCESS_KEY")
PAAPI_SECRET_KEY = os.getenv("PAAPI_SECRET_KEY")
PAAPI_PARTNER_TAG = os.getenv("PAAPI_PARTNER_TAG")
PAAPI_HOST = os.getenv("PAAPI_HOST")
PAAPI_REGION = os.getenv("PAAPI_REGION")

# Fetch products from Amazon PA-API
def fetch_amazon_products():
    url = f"https://{PAAPI_HOST}/paapi5/searchitems"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Amz-Target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"
    }
    
    # Request payload
    payload = {
        "PartnerTag": PAAPI_PARTNER_TAG,
        "Keywords": "computers electronics bikes machines patio",
        "Marketplace": "www.amazon.com",
        "ItemCount": 10,
        "Resources": [
            "ItemInfo.Title",
            "ItemInfo.Features",
            "Images.Primary.Medium",
            "Offers.Listings.Price",
            "Offers.Listings.SavingBasis",
            "Offers.Listings.Availability",
            "BrowseNodeInfo.WebsiteSalesRank"
        ]
    }
    
    # Send the request to Amazon's PA-API
    response = requests.post(url, headers=headers, json=payload, auth=(PAAPI_ACCESS_KEY, PAAPI_SECRET_KEY))
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("SearchResult", {}).get("Items", [])
        # Filter items based on price and sales rank
        filtered_items = []
        for item in items:
            price = item.get("Offers", {}).get("Listings", [{}])[0].get("Price", {}).get("DisplayAmount", "").replace('$', '').replace(',', '')
            price = float(price) if price else 0
            sales_rank = item.get("BrowseNodeInfo", {}).get("WebsiteSalesRank", {}).get("SalesRank", 0)
            
            # Filter products within price range and with valid sales rank
            if 500 <= price <= 5000 and sales_rank > 0:
                filtered_items.append(item)
        
        return filtered_items
    else:
        print(f"Error fetching products: {response.status_code}")
        return []

# Example usage
if __name__ == "__main__":
    products = fetch_amazon_products()
    for product in products:
        title = product.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "")
        price = product.get("Offers", {}).get("Listings", [{}])[0].get("Price", {}).get("DisplayAmount", "")
        url = product.get("DetailPageURL", "")
        print(f"Title: {title}, Price: {price}, Link: {url}")
