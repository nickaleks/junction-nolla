from flask import Flask
from flask_cors import CORS
from flask import request
import flask
import json
import model

app = Flask(__name__)
CORS(app)   

def serialize_not_none(obj):
    if obj is None:
        return {'error': 'entity not found' }, 404
    else:
        return json.dumps(obj)

@app.route('/inbox/<user_id>')
def inbox(user_id):
    return serialize_not_none(model.get_inbox(user_id))

@app.route('/action/create', methods=['POST'])
def create_action():
    return model.create_action(json.loads(request.data))

if __name__ == '__main__':
    app.run(host='0.0.0.0')