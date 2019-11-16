import requests

cached_stores = []

def store_search(filters):
    root_url = "https://kesko.azure-api.net/v1/search/stores"
    headers = {"Ocp-Apim-Subscription-Key": "f2d58b3f3e1a48ce8c1cef544eeef668"}
    query_body = dict()
    query_body['filters'] = filters
    r = requests.post(root_url, json=query_body, headers = headers)
    return r

def get_product_details(store_id, ean):
    root_url = f"https://kesko.azure-api.net/products/{store_id}/{ean}"
    headers = {"Ocp-Apim-Subscription-Key": "f2d58b3f3e1a48ce8c1cef544eeef668"}
    r = requests.get(root_url, headers = headers)
    return r

def get_store_id(store):
    return store['Id']

def get_helsinki_stores():
    global cached_stores
    if cached_stores:
        return cached_stores
    else:
        stores = store_search({'municipality': 'HELSINKI'}).json()['results']
        store_ids = list(map(get_store_id, stores))
        cached_stores = store_ids
        return cached_stores

def search_product_details(ean):
    for store_id in get_helsinki_stores():
        details = get_product_details(store_id, ean)
        if details:
            return details.json()
