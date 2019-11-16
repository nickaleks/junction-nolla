import requests 


def get_product_by_ean(ean):
    root_url = "https://kesko.azure-api.net/v1/search/products"
    headers = {"Ocp-Apim-Subscription-Key": "f2d58b3f3e1a48ce8c1cef544eeef668"}
    query_body = dict()
    query_body['filters'] = {"ean" : str(ean)}    
    r = requests.post(root_url, json=query_body, headers = headers)

    product_json = r.json()
    if product_json['totalHits'] == 0:
        return None

    if product_json['isConsumerGood']:
        return None

    return extract_properties(product_json['results'][0])

attributes_to_extract = ["ENERKC", "ENERKJ", "KUITUA", "NTGEW", "PROTEG", "RASVAA", "SOKERI", "SUOLA", "HIHYDR", "ALKPI", "DVITAM"]
def extract_properties(product_json):
    
    ean = product_json['ean']
    name = product_json['marketingName']['finnish']
    is_alcohol = product_json['isAlcohol']
    brand = product_json['brand']
    picture_url = product_json['pictureUrls'][0]['original']
    category_id = product_json['category']['id']
    subcategory_id = product_json['subcategory']['id']    

    if 'TX_RAVOMI' in product_json['attributes']:
        n_properties = " ".join(filter(lambda x: x, [x.get('abbreviation', None) for x in product_json['attributes']['TX_RAVOMI']['value']]))
    else:
        n_properties = []
    manufacturer = product_json['attributes']['ZZVENDOR']['value']['explanation']['finnish']

    def get_attribute(attribute_name):
        if attribute_name in product_json['attributes']:
            return product_json['attributes'][attribute_name]['value']['value'] 
        else:
            return None    
    attributes = dict(zip(attributes_to_extract, map(get_attribute, attributes_to_extract)))
    
    alcohol_content = attributes['ALKPI']
    vitamin_d = attributes['DVITAM']
    energy_kcal = attributes['ENERKC']
    enerjy_kj = attributes['ENERKJ']
    fiber = attributes['KUITUA']
    protein = attributes['PROTEG']
    fats = attributes['RASVAA']
    sugars = attributes['SOKERI']
    salt = attributes['SUOLA']
    carbs = attributes['HIHYDR']
    weight = attributes['NTGEW']


    
    fetched_attributes = locals()
    del fetched_attributes['product_json']
    del fetched_attributes['attributes']
    del fetched_attributes['get_attribute']
    
    return fetched_attributes
    