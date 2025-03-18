import requests
import time
import pandas as pd

# Token
AUTH_TOKEN = "Bearer APP_USR-6653595949052997-031809-c77a6ab1194c9e79f3dd3beb3eb41b2a-706911790"
HEADERS = {"Authorization": AUTH_TOKEN}

# Configuración
SEARCH_TERMS = ["Samsung S24", "Moto Edge 50", "iPhone 15", "Xiaomi Redmi Note 14"]
ITEMS_PER_TERM = 50  # 50 items por producto
DELAY = 1  # 1 segundo entre requests

def fetch_items(search_term):
    item_ids = []
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={search_term}&limit={ITEMS_PER_TERM}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return [item['id'] for item in data['results'][:ITEMS_PER_TERM]]  # Limitado a 50
    else:
        print(f"Error en {search_term}: {response.text}")
        return []

def fetch_item_details(item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def main():
    all_items = []
    for term in SEARCH_TERMS:
        print(f"Obteniendo {ITEMS_PER_TERM} ítems para: {term}")
        item_ids = fetch_items(term)
        for item_id in item_ids:
            item = fetch_item_details(item_id)
            if item:
                all_items.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "condition": item.get("condition"),
                    "category_id": item.get("category_id"),
                    "listing_type": item.get("listing_type_id"),
                    "free_shipping": item.get("shipping", {}).get("free_shipping", False),
                })
            time.sleep(DELAY)  # Evitar rate limits
    
    # Guardar CSV
    df = pd.DataFrame(all_items)
    df.to_csv("mercadolibre_products.csv", index=False)
    print(f"¡Listo! CSV generado con {len(df)} productos.")

if __name__ == "__main__":
    main()