def get_product_by_ean(ean):
    root_url = "https://kesko.azure-api.net/v1/search/products"
    headers = {"Ocp-Apim-Subscription-Key": "f2d58b3f3e1a48ce8c1cef544eeef668"}
    query_body = dict()
    query_body['filters'] = {"ean" : str(ean)}    
    r = requests.post(root_url, json=query_body, headers = headers)

    r_json = r.json()
    
    if r_json['totalHits'] == 0:
        return None
    
    product_json = r_json['results'][0]
    
    if product_json['isConsumerGood']:
        return None
    
#     pprint.pprint(product_json, width=250)

    return extract_properties(product_json)

attributes_to_extract = ["ENERKC", "ENERKJ", "KUITUA", "NTGEW", "PROTEG", "RASVAA", "SOKERI", "SUOLA", "HIHYDR", "ALKPI", "DVITAM"]
def extract_properties(product_json):
    
    ean = product_json['ean']
    name = product_json['marketingName']['finnish']
    is_alcohol = product_json['isAlcohol']
    brand = product_json.get('brand', None)
    picture_url = product_json['pictureUrls'][0]['original'] if product_json['pictureUrls'] else None
    category_id = product_json['category']['id']
    subcategory_id = product_json['subcategory']['id']    

    if 'TX_RAVOMI' in product_json['attributes']:
        properties = product_json['attributes']['TX_RAVOMI']['value']
#         print(properties)
        if type(properties) == list:
            n_properties = " ".join(filter(lambda x: x, [x.get('abbreviation', None) for x in properties]))
        else:
            n_properties = properties['abbreviation']
    else:
        n_properties = []
        
    if 'ZZVENDOR' in product_json['attributes']:
        manufacturer = product_json['attributes']['ZZVENDOR']['value']['explanation']['finnish']
    else:
        manufacturer = None

    def get_attribute(attribute_name):
        if attribute_name in product_json['attributes']:
            if 'value' in product_json['attributes'][attribute_name]:
                return product_json['attributes'][attribute_name]['value']['value'] 
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
    if 'properties' in fetched_attributes:
        del fetched_attributes['properties']
    
    return fetched_attributes
    