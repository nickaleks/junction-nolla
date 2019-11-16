def get_product_by_ean(ean):
    root_url = "https://kesko.azure-api.net/v1/search/products"
    headers = {"Ocp-Apim-Subscription-Key": "f2d58b3f3e1a48ce8c1cef544eeef668"}
    query_body = dict()
    query_body['filters'] = {"ean" : str(ean)}    
    r = requests.post(root_url, json=query_body, headers = headers)

    product_json = r.json()
    if product_json['totalHits'] == 0:
        return None
    return extract_properties(product_json['results'][0])

def extract_properties(product_json):
    
    ean = product_json['ean']
    name = product_json['marketingName']['finnish']
    brand = product_json['brand']
    manufacturer = product_json['attributes']['ZZVENDOR']['value']['explanation']['finnish']
    weight = product_json['attributes']['NTGEW']['value']['value'] 
    n_properties = " ".join(filter(lambda x: x, [x.get('abbreviation', None) for x in product_json['attributes']['TX_RAVOMI']['value']]))
    is_alcohol = product_json['isAlcohol']
    alcohol_content = product_json['attributes'].get('ALKPI', None)
    vitamin_d = product_json['attributes'].get('DVITAM', None)
    energy_kcal = product_json['attributes']['ENERKC']['value']['value'] 
    enerjy_kj = product_json['attributes']['ENERKJ']['value']['value'] 
    fiber = product_json['attributes']['KUITUA']['value']['value'] 
    protein = product_json['attributes']['PROTEG']['value']['value']
    fats = product_json['attributes']['RASVAA']['value']['value'] 
    sugars = product_json['attributes']['SOKERI']['value']['value'] 
    salt = product_json['attributes']['SUOLA']['value']['value'] 
    carbs = product_json['attributes']['HIHYDR']['value']['value'] 
    picture_url = product_json['pictureUrls'][0]['original']
    category_id = product_json['category']['id']
    subcategory_id = product_json['subcategory']['id']
    
    fetched_attributes = locals()
    del fetched_attributes['product_json']
    
    return fetched_attributes