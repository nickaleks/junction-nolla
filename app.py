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

@app.route('/user/<user_id>')
def get_user(user_id):
    return serialize_not_none(model.get_user(user_id))

@app.route('/user/<user_id>/daily_goal')
def get_user_goal(user_id):
    return serialize_not_none(model.get_daily_goal_progress(model.get_user(user_id)))

@app.route('/user/<user_id>/waste/<granularity>')
def get_user_waste(user_id, granularity):
    if granularity in model.granularity:
        return serialize_not_none(model.get_waste(user_id, granularity))
    else:
        return {'error': 'entity not found' }, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')
