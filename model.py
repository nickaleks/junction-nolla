import psycopg2
con = psycopg2.connect(database="postgres", user="postgres", password="mysecretpassword", host="40.118.124.20", port="5432")

def get_inbox(user_id):
    return {
        'products': [
        ],
        'recipes': [],
        'daily_goal': {
            'required': 3000,
            'done': 1300
        }
    }

def get_user(user_id):
    query = f"SELECT id, customer_id FROM customer WHERE id = {user_id}"
    cursor = con.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    return {'id': user[0], 'customer_id': user[1] }
