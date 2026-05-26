"""
Advanced Production-Grade API Scraper with Pagination
Fetches ALL products from DummyJSON by iterating through pages automatically.
"""

import requests
from typing import Dict, List, Optional
import time

def fetch_api_data(url: str, skip: int = 0, limit: int = 30, timeout: int = 10) -> Optional[Dict]:
    """
    Fetch JSON data from API with pagination support using 'limit' and 'skip'.
    """
    # Kendimizi tarayıcı gibi tanıtıyoruz
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }
    
    # URL'nin sonuna ?limit=30&skip=0 gibi eklemeleri requests kütüphanesi yapar
    params = {
        'limit': limit,
        'skip': skip,
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data (skip={skip}): {e}")
        return None

def extract_product_data(products: List[Dict]) -> List[Dict]:
    """
    Extract relevant fields from the raw product list safely.
    """
    extracted_data = []
    
    for product in products:
        extracted_product = {
            'id': product.get('id'),
            'title': product.get('title'),
            'price': product.get('price'),
            'rating': product.get('rating'),
            # Eğer kategori yoksa 'N/A' yazsın (Defensive Programming)
            'category': product.get('category', 'N/A'),
        }
        extracted_data.append(extracted_product)
    
    return extracted_data

def print_product_data(products: List[Dict]) -> None:
    """
    Print a list of products in a clean format.
    """
    print("-" * 50)
    for idx, product in enumerate(products, 1):
        print(f"Product ID: {product['id']}")
        print(f"Title:      {product['title']}")
        print(f"Price:      ${product['price']}")
        print(f"Rating:     {product['rating']}")
        print(f"Category:   {product['category']}")
        print("-" * 50)

def main() -> None:
    """
    Main function: Controls the infinite loop to fetch ALL pages.
    """
    api_url = "https://dummyjson.com/products"
    
    all_raw_products = [] # Ham verileri burada biriktireceğiz
    limit = 30            # Her seferde 30 ürün iste
    skip = 0              # 0'dan başla
    total = 0             # Toplam ürün sayısını ilk istekte öğreneceğiz

    print(f"🚀 Starting scraper for: {api_url}\n")

    # --- PAGINATION DÖNGÜSÜ (SONSUZ DÖNGÜ) ---
    while True:
        print(f"📥 Fetching batch... (Skip: {skip}, Limit: {limit})")
        
        # 1. API'ye İsteği At
        data = fetch_api_data(api_url, skip=skip, limit=limit)
        
        # Eğer veri gelmezse veya hata olursa dur
        if not data:
            print("❌ Error: No data returned. Stopping.")
            break

        # 2. Gelen paketin içindeki ürünleri al
        products_batch = data.get('products', [])
        
        if not products_batch:
            print("⚠️ No more products found in this batch.")
            break
            
        # 3. Listeye Ekle (Extend)
        all_raw_products.extend(products_batch)
        
        # 4. Toplam Hedef Sayısını Öğren (Sadece ilk turda çalışır)
        if total == 0:
            total = data.get('total', 0)
            print(f"🎯 TARGET: Total {total} products found in database.")

        # 5. İlerleme Raporu
        print(f"✅ Progress: {len(all_raw_products)} / {total} products collected.")

        # 6. ÇIKIŞ KOŞULU: Eğer topladığımız sayı, toplam sayıya ulaştıysa DUR.
        if len(all_raw_products) >= total:
            print("\n🎉 SUCCESS: All products collected!")
            break
            
        # 7. Bir sonraki sayfa için skip değerini artır
        skip += limit
        
        # Sunucuyu yormamak için minik bir bekleme (opsiyonel ama kibar)
        time.sleep(0.5)

    # --- SONUÇLARI İŞLE VE GÖSTER ---
    print("\n" + "="*70)
    print(f"FINAL REPORT: Total {len(all_raw_products)} products scraped.")
    print("="*70)
    
    # Hepsini ayıkla (Extraction)
    clean_products = extract_product_data(all_raw_products)
    
    # Ekrana hepsini basmak çok uzun sürer, sadece SON 5 tanesini gösterelim
    # (Böylece 194. ürüne ulaşıp ulaşmadığımızı kanıtlamış oluruz)
    print("\nDisplaying the LAST 5 products as proof:\n")
    print_product_data(clean_products[-5:])

if __name__ == "__main__":
    main()