from flask import Flask
from flask_cors import CORS
import json
import model

app = Flask(__name__)
CORS(app)   

@app.route('/inbox/<user_id>')
def hello_world(user_id):
    return json.dumps(model.get_user(user_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0')