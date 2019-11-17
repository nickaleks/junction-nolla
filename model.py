import psycopg2
import api
from datetime import datetime, timedelta
from expiration_date import get_shelf_time
import functools
con = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="40.118.124.20", port="5432")

action_buy = "ACTION_BUY"
action_eat = "ACTION_EAT"
action_lose = "ACTION_LOSE"
action_waste = "ACTION_WASTE"

granularity = ["day","week", "month", "year"]

def get_inbox(user_id):
    # process_receipts(user_id)
    user = get_user(user_id)
    current_products = get_current_products(user_id)
    daily_goal = get_daily_goal_progress(user)
    return {'products': [prod for prod in current_products if prod['amount_left'] > 0], 'recipes': [], 'daily_goal': daily_goal}

def get_user(user_id):
    query = f"SELECT id, customer_id, name, daily_goal_id FROM customer WHERE id = {user_id}"
    cursor = con.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    con.commit()
    cursor.close()
    if not user:
        return None
    return {'id': user[0], 'customer_id': user[1], 'name': user[2], 'daily_goal_id': user[3] }

def is_today(date):
    d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    return d.date() == datetime.today().date()

def get_daily_goal_progress(user):
    query = f"SELECT calories, carbs, fats, proteins FROM daily_goal WHERE id = {user['daily_goal_id']}"
    cursor = con.cursor()
    cursor.execute(query)
    calories, carbs, fats, proteins = cursor.fetchone()
    con.commit()
    cursor.close()
    actions = get_user_actions(user['id'])
    calories_progress = 0
    carbs_progress = 0
    fat_progress = 0
    protein_progress = 0

    for action in actions:
        if action['action_type'] == action_eat and is_today(action['action_date']):
            product = get_product_by_id(action['product_id'])
            # kcal / 100 * weight * quantity
            weight = float(product['weight'] * 1000)
            quantity = action['amount']
            cal = float(product['energy_kcal'])
            eaten_calories = int(cal / 100.0  * quantity)
            eaten_carbs = int(float(product['carbs']) / 100.0 * quantity)
            eaten_fats = int(float(product['fats']) / 100.0 * quantity)
            eaten_prot = int(float(product['protein']) / 100.0 * quantity)
            calories_progress += eaten_calories
            carbs_progress += eaten_carbs
            fat_progress += eaten_fats
            protein_progress += eaten_prot

    return {
        'calories': {
            'total': calories,
            'progress': calories_progress
        },
        'carbs': {
            'total': carbs,
            'progress': carbs_progress
        },
        'fats': {
            'total': fats,
            'progress': fat_progress
        },
        'proteins': {
            'total': proteins,
            'progress': protein_progress
        }
    }


def get_product_by_id(product_id):
    query = f"""SELECT 
    id,
    ean ,
    name ,
    brand ,
    manufacturer ,
    weight,
    n_properties,
    is_alcohol,
    alcohol_content,
    vitamin_d ,
    energy_kcal ,
    enerjy_kj ,
    fiber ,
    protein ,
    fats ,
    sugars ,
    salt ,
    carbs ,
    picture_url ,
    category_id ,
    subcategory_id,
    price,
    shelf_time FROM product WHERE id = {product_id}"""
    cursor = con.cursor()
    cursor.execute(query)
    product = cursor.fetchone()
    con.commit()
    cursor.close()
    return {
        'id': product[0],
        'ean': product[1],
        'name': product[2] ,
        'brand': product[3] ,
        'manufacturer': product[4] ,
        'weight': product[5],
        'n_properties': product[6],
        'is_alcohol': product[7],
        'alcohol_content': product[8],
        'vitamin_d': product[9],
        'energy_kcal': product[10],
        'enerjy_kj': product[11],
        'fiber': product[12],
        'protein': product[13],
        'fats': product[14],
        'sugars': product[15],
        'salt': product[16],
        'carbs': product[17],
        'picture_url': product[18],
        'category_id': product[19],
        'subcategory_id': product[20],
        'price': product[21],
        'shelf_time': product[22]
    }

def calc_exp_time(action):
    today = datetime.today()
    created_at = action.get('action_date')
    created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')
    delta = today - created_at
    product_id = action['product_id']
    shelf_time = get_product_by_id(product_id)['shelf_time']
    return shelf_time - delta.days

def get_current_products(user_id):
    actions = get_user_actions(user_id)
    purchases = {}
    for action in actions:
        if action['action_type'] == action_buy:
            purchases[action['purchase_id']] = {
                'product': get_product_by_id(action['product_id']),
                'amount_left': action['amount'],
                'purchase_id': action['purchase_id'],
                'exp_time': calc_exp_time(action)}

    for action in actions:
        if action['action_type'] != action_buy:
            if purchases[action['purchase_id']]:
                purchases[action['purchase_id']]['amount_left'] -= action['amount']

    return list(purchases.values())

def parse_actions(action_row):
    return {
        'id': action_row[0],
        'customer_id': action_row[1],
        'action_type': action_row[2],
        'product_id': action_row[3],
        'amount': action_row[4],
        'purchase_id': action_row[5],
        'action_date': action_row[6],
        'karma': action_row[7]
    }

def get_user_actions(user_id):
    query = f"SELECT id, customer_id, action_type, product_id, amount, purchase_id, action_date, karma FROM action WHERE customer_id = {user_id}"
    cursor = con.cursor()
    cursor.execute(query)
    actions = cursor.fetchall()
    con.commit()
    cursor.close()

    return [parse_actions(action) for action in actions]

def get_user_receipts(customer_id):
    
    query = f"SELECT id, receipt_id, customer_id, ean, transaction_date, quantity FROM receipt WHERE customer_id = {customer_id}"
    cursor = con.cursor()
    cursor.execute(query)
    actions = cursor.fetchall()
    con.commit()
    cursor.close()
    return [{
        'id': action[0], 
        'receipt_id': action[1], 
        'customer_id': action[2], 
        'ean': action[3], 
        'transaction_date': action[4], 
        'quantity': action[5]
    } for action in actions]

def add_product(product):
    query = """INSERT INTO product (
    ean ,
    name ,
    brand ,
    manufacturer ,
    weight,
    n_properties,
    is_alcohol,
    alcohol_content,
    vitamin_d ,
    energy_kcal ,
    enerjy_kj ,
    fiber ,
    protein ,
    fats ,
    sugars ,
    salt ,
    carbs ,
    picture_url ,
    category_id ,
    subcategory_id ,
    price ,
    shelf_time)
    VALUES (
    %(ean)s,
    %(name)s,
    %(brand)s,
    %(manufacturer)s,
    %(weight)s,
    %(n_properties)s,
    %(is_alcohol)s,
    %(alcohol_content)s,
    %(vitamin_d)s,
    %(energy_kcal)s,
    %(enerjy_kj)s,
    %(fiber)s,
    %(protein)s,
    %(fats)s,
    %(sugars)s,
    %(salt)s,
    %(carbs)s,
    %(picture_url)s,
    %(category_id)s,
    %(subcategory_id)s,
    %(price)s,
    %(shelf_time)s) RETURNING id
    """
    cursor = con.cursor()
    cursor.execute(query, product)
    con.commit()
    cursor.close()

def get_product(ean):
    query = f"""SELECT 
    id,
    ean ,
    name ,
    brand ,
    manufacturer ,
    weight,
    n_properties,
    is_alcohol,
    alcohol_content,
    vitamin_d ,
    energy_kcal ,
    enerjy_kj ,
    fiber ,
    protein ,
    fats ,
    sugars ,
    salt ,
    carbs ,
    picture_url ,
    category_id ,
    subcategory_id,
    price,
    shelf_time FROM product WHERE ean = {ean}"""
    cursor = con.cursor()
    cursor.execute(query)
    product = cursor.fetchone()
    con.commit()
    cursor.close()
    return {
        'id': product[0],
        'ean': product[1],
        'name': product[2] ,
        'brand': product[3] ,
        'manufacturer': product[4] ,
        'weight': product[5],
        'n_properties': product[6],
        'is_alcohol': product[7],
        'alcohol_content': product[8],
        'vitamin_d': product[9],
        'energy_kcal': product[10],
        'enerjy_kj': product[11],
        'fiber': product[12],
        'protein': product[13],
        'fats': product[14],
        'sugars': product[15],
        'salt': product[16],
        'carbs': product[17],
        'picture_url': product[18],
        'category_id': product[19],
        'subcategory_id': product[20],
        'price': product[21],
        'shelf_tife': product[22]
    }

def add_action(action):
    query = """INSERT INTO action (
    customer_id ,
    action_type ,
    purchase_id ,
    product_id,
    amount,
    action_date,
    karma) 
    VALUES (
    %(customer_id)s ,
    %(action_type)s ,
    %(purchase_id)s ,
    %(product_id)s,
    %(amount)s,
    %(action_date)s,
    0) RETURNING id
    """
    cursor = con.cursor()
    cursor.execute(query, action)
    con.commit()
    cursor.close()

def process_receipts(user_id):
    customer = get_user(user_id)['customer_id']
    receipts = get_user_receipts(customer)
    product_ids = []
    for receipt in receipts:
        try:
            product = api.get_product_by_ean(receipt['ean'])
            product_ids.append(add_product(product))
        except:
            print("failed to insert")
            con.rollback()
            pass
        product = get_product(receipt['ean'])
        action = {
            'customer_id': customer,
            'action_type': action_buy,
            'purchase_id': receipt['id'],
            'action_date': receipt['transaction_date'],
            'product_id': product['id'],
            'amount': receipt['quantity'] * int(product['weight'] * 1000)
        }
        add_action(action)
        
    return product_ids

def create_action(action):
    add_action(action)
    goals = get_daily_goal_progress(get_user(1))
    total = goals['calories']['total']
    progress = goals['calories']['progress']
    # 'calories': {
    #         'total': calories,
    #         'progress': calories_progress
    #     },
    print(goals)
    if action['action_type'] == action_eat and progress > total:
        update_action(action, -2)
        return {
            'has_message': action['action_type'] == action_eat and progress > total,
            'message': 'You have exceeded your daily limit',
            'karma': -2
        }
    else:
        return {
            'has_message': False,
            'message':'',
            'karma': 0
        }

def update_price(ean, price):
    query = f"""UPDATE product
    SET price = {price}
    WHERE ean = {ean}"""
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()

def update_action(action, karma):
    query = f"""update action set karma = {karma} 
    where purchase_id = {action['purchase_id']} 
    and product_id = {action['product_id']}"""
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    cursor.close()

def get_delta(granularity):
    today = datetime.today()
    d = 0
    if granularity == "day":
        d = today - timedelta(days=75)
    elif granularity == "week":
        d = today - timedelta(days=82)
    elif granularity == "month":
        d = today - timedelta(days = 105)
    elif granularity == "year":
        d = today - timedelta(days = 365)
    return d.strftime('%Y-%m-%d %H:%M:%S.%f')

def add_price(action):
    action['product'] = get_product_by_id(action['product_id'])
    price = 0
    if action['product']['weight'] !=0.0:
        price = action['product']['price']*action['amount']/(action['product']['weight']*1000)
    else:
        price = 0
    action['price'] = price
    return action

def prepare_res(res):
    resp = {}
    for action in res:
        product_id = action['product_id']
        stored = resp.get(product_id)
        if stored:
            stored['price'] = stored['price']+action['price']
            resp[product_id] = stored
        else:
            product = action['product']
            product['price'] = action['price']
            resp[product_id] = product
    return list(resp.values())

def get_waste(user_id, granularity):
    actions = get_user_actions(user_id)
    delta = get_delta(granularity)
    filter_by_period = list(filter(lambda x: x['action_date'] >= delta, actions))
    actions_with_price = list(map(add_price, filter_by_period))
    waste =list(filter(lambda x: x['action_type'] == action_waste, actions_with_price))
    waste_sum = functools.reduce(lambda x,y :x + y['price'],waste, 0.0)
    all_sum = functools.reduce(lambda x,y : x + y['price'],actions_with_price, 0.0)

    ratio = 0.0
    if all_sum!=0:
        ratio = waste_sum/all_sum

    response = {}
    response['result'] = prepare_res(waste)
    response['sum'] = waste_sum
    response['ratio'] = ratio
    response['total'] = len(waste)
    return response

def get_karma(user_id):
    actions = get_user_actions(user_id)
    karma = list(filter(lambda x: x['karma'] != 0, actions))
    response = {}
    response['result'] = karma
    response['sum'] = functools.reduce(lambda x,y : x + y['karma'],karma, 0)
    response['total'] = len(karma)
    return response
