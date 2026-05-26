

import requests
from typing import Dict, List, Optional
import json


def fetch_api_data(url: str, timeout: int = 10, use_mock: bool = False) -> Optional[Dict]:
    """
    Fetch JSON data from the specified API endpoint.
    
    Args:
        url: The API endpoint URL
        timeout: Request timeout in seconds (default: 10)
        use_mock: If True, return mock data for demonstration (default: False)
    
    Returns:
        Parsed JSON response as a dictionary, or None if request fails
    
    Raises:
        requests.exceptions.RequestException: For network-related errors
    """
    # Mock data for demonstration purposes
    if use_mock:
        print("(Using mock data for demonstration)")
        return {
            "products": [
                {"id": 1, "title": "iPhone 9", "price": 549, "rating": 4.69},
                {"id": 2, "title": "iPhone X", "price": 899, "rating": 4.44},
                {"id": 3, "title": "Samsung Universe 9", "price": 1249, "rating": 4.09},
                {"id": 4, "title": "OPPOF19", "price": 280, "rating": 4.3},
                {"id": 5, "title": "Huawei P30", "price": 499, "rating": 4.09},
            ],
            "total": 100,
            "skip": 0,
            "limit": 30
        }
    
    # Set User-Agent header to identify our client and avoid potential blocking
    # Many APIs require or prefer a custom User-Agent over the default requests UA
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',  # Explicitly request JSON response
    }
    
    try:
        # Make GET request with timeout to prevent hanging indefinitely
        # Timeout is critical in production to handle unresponsive servers
        response = requests.get(url, headers=headers, timeout=timeout)
        
        # Raise an exception for 4xx/5xx status codes
        # This allows us to handle errors explicitly rather than processing bad responses
        response.raise_for_status()
        
        # Parse JSON response directly using response.json()
        # WHY response.json() instead of BeautifulSoup:
        # - This API returns JSON data, not HTML markup
        # - response.json() is the native, efficient way to parse JSON in requests
        # - BeautifulSoup is designed for HTML/XML parsing, not JSON
        # - Using response.json() is faster, cleaner, and more maintainable for JSON APIs
        return response.json()
    
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout} seconds")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON response: {e}")
        return None


def extract_product_data(products: List[Dict], limit: int = 5) -> List[Dict]:
    """
    Extract relevant fields from the product list.
    
    Args:
        products: List of product dictionaries from the API
        limit: Number of products to extract (default: 5)
    
    Returns:
        List of dictionaries containing only id, title, price, and rating
    """
    extracted_data = []
    
    # Process only the first 'limit' products
    for product in products[:limit]:
        # Extract only the required fields
        # Using .get() with defaults to handle missing fields gracefully
        extracted_product = {
            'id': product.get('id'),
            'title': product.get('title'),
            'price': product.get('price'),
            'rating': product.get('rating'),
        }
        extracted_data.append(extracted_product)
    
    return extracted_data


def print_product_data(products: List[Dict]) -> None:
    """
    Print extracted product data in a clean, readable format.
    
    Args:
        products: List of product dictionaries to display
    """
    print("\n" + "="*70)
    print("EXTRACTED PRODUCT DATA")
    print("="*70)
    
    for idx, product in enumerate(products, 1):
        print(f"\nProduct {idx}:")
        print(f"  ID:     {product['id']}")
        print(f"  Title:  {product['title']}")
        print(f"  Price:  ${product['price']}")
        print(f"  Rating: {product['rating']}")
    
    print("\n" + "="*70)


def main() -> None:
    """
    Main execution function.
    
    Orchestrates the API fetching, data extraction, and display process.
    """
    # API endpoint for DummyJSON products
    api_url = "https://dummyjson.com/products"
    
    print(f"Fetching data from: {api_url}")
    
    # Fetch data from the API (using mock data for demo)
    api_response = fetch_api_data(api_url, use_mock=True)
    
    if api_response is None:
        print("Failed to fetch data from the API. Exiting.")
        return
    
    # Extract the products list from the response
    # DummyJSON returns products in a 'products' key
    products = api_response.get('products', [])
    
    if not products:
        print("No products found in the API response.")
        return
    
    print(f"Successfully fetched {len(products)} products from the API")
    
    # Extract only the required fields from the first 5 products
    extracted_products = extract_product_data(products, limit=5)
    
    # Display the extracted data
    print_product_data(extracted_products)


if __name__ == "__main__":
    main()