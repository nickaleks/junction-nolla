from datetime import datetime

food_categories = {
    '30': 360,
    '40': 180,
    '35': 360,
    '11': 10,
    '13': 360,
    '15': 7,
    '20': 14,
    '25': 1440,
    '45': 270,
    '14': 60,
    '8' : 14
}

food_subcategories = {
    '355': 90,
    '403': 360,
    '350': 720,
    '100': 7,
    '101': 7,
    '102': 14,
    '105': 90,
    '208': 90,
    '134': 2, #sosiski
    '110': 3,
    '150': 7,
    '155': 1800,
    '157': 21,
    '158': 10,
    '136': 14,
    '106': 30,
    '146': 60,
    '109': 150,
    '250': 720,
    '103': 5,
    '201': 180,
    '131': 2,
    '400': 21,
    '304': 720
}

def get_shelf_time(product):
    category = str(product.get('category', {}).get('id'))
    subcategory = str(product.get('subcategory', {}).get('id'))
    if subcategory in food_subcategories:
        return food_subcategories[subcategory]

    if category in food_categories:
        return food_categories[category]

    return 600

def calc_exp_time(product):
    today = datetime.today()
    created_at = product.get('transaction_date') or today #check that transaction date in datetime
    delta = today - created_at
    return get_shelf_time(product) - delta.days

def add_shelf_and_exp_time(product):
    upd = {'shelf_time': get_shelf_time(product),
           'exp_time': calc_exp_time(product)}
    product.update(upd)
    return product

#list(map(add_shelf_and_exp_time, [{}]))
