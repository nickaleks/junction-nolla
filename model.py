import psycopg2
import api
con = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="40.118.124.20", port="5432")

action_buy = "ACTION_BUY"
action_eat = "ACTION_EAT"
action_lose = "ACTION_LOSE"
action_throw_away = "ACTION_THROW_AWAY"


def get_inbox(user_id):
    # process_receipts(user_id)
    user = get_user(user_id)
    current_products = get_current_products(user_id)
    return {'products': current_products, 'recipes': [], 'daily_goal': {}}
    # return process_receipts(user_id)

def get_user(user_id):
    query = f"SELECT id, customer_id FROM customer WHERE id = {user_id}"
    cursor = con.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    if not user:
        return None
    return {'id': user[0], 'customer_id': user[1] }

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
    subcategory_id FROM product WHERE id = {product_id}"""
    cursor = con.cursor()
    cursor.execute(query)
    product = cursor.fetchone()
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
        'subcategory_id': product[20]
    }


def get_current_products(user_id):
    actions = get_user_actions(user_id)
    purchases = {}
    for action in actions:
        if action['action_type'] == action_buy:
            purchases[action['purchase_id']] = {'product': get_product_by_id(action['product_id']), 'amount_left': action['amount']}
    
    for action in actions:
        if action['action_type'] != action_buy:
            if purchases[action['purchase_id']]:
                purchases[action['purchase_id']]['amount_left'] -= action['amount']
            
    return list(purchases.values())

def get_user_actions(user_id):
    query = f"SELECT id, customer_id, action_type, product_id, amount, purchase_id, action_date FROM action WHERE customer_id = {user_id}"
    cursor = con.cursor()
    cursor.execute(query)
    actions = cursor.fetchall()
    cursor.close()

    return [parse_actions(action) for action in actions]

def parse_actions(action_row):
    return {
        'id': action_row[0],
        'customer_id': action_row[1],
        'action_type': action_row[2],
        'product_id': action_row[3],
        'amount': action_row[4],
        'purchase_id': action_row[5],
        'action_date': action_row[6]
    }

def get_user_receipts(customer_id):
    
    query = f"SELECT id, receipt_id, customer_id, ean, transaction_date, quantity FROM receipt WHERE customer_id = {customer_id}"
    cursor = con.cursor()
    cursor.execute(query)
    actions = cursor.fetchall()
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
    subcategory_id) 
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
    %(subcategory_id)s) RETURNING id
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
    subcategory_id FROM product WHERE ean = {ean}"""
    cursor = con.cursor()
    cursor.execute(query)
    product = cursor.fetchone()
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
        'subcategory_id': product[20]
    }

def add_action(action):
    query = """INSERT INTO action (
    customer_id ,
    action_type ,
    purchase_id ,
    product_id,
    amount,
    action_date) 
    VALUES (
    %(customer_id)s ,
    %(action_type)s ,
    %(purchase_id)s ,
    %(product_id)s,
    %(amount)s,
    %(action_date)s) RETURNING id
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
        action = {
            'customer_id': customer,
            'action_type': action_buy,
            'purchase_id': receipt['id'],
            'action_date': receipt['transaction_date'],
            'product_id': get_product(receipt['ean'])['id'],
            'amount': receipt['quantity']
        }
        # print(action)
        add_action(action)
        
    return product_ids

def create_action(action):
    add_action(action)
    return {}