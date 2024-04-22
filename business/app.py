from flask import Flask, jsonify, request, Blueprint
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Blueprint('api', __name__)

client = MongoClient("mongodb+srv://root:root@event-mgmt.3fujjxh.mongodb.net/?retryWrites=true&w=majority&appName=event-mgmt")
db = client["event-mgmt"]

users = db['users']
user_schema = {
    "userid": str,
    "password": str,
    "genre": str,
    "objects": [dict]
}

events = db['events']
event_schema = {
    "event_name": str,
    "location": str,
    "date": str,
    "genre": str
}

class UserManagement:
    @staticmethod
    @api.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        print("api hit successful")
        user = users.find_one({'userid': username, 'password': password})

        if user:
            return jsonify({"message": "Login successful"}), 200
        else:
            print("user not found")
            return jsonify({"message": "Invalid username or password"}), 401
    
    @staticmethod
    @api.route('/add_user', methods=['POST'])
    def add_user():
        user_data = request.json
        users.insert_one(user_data)
        return jsonify({"message": "User added successfully!"})

    @staticmethod
    @api.route('/get_users', methods=['GET'])
    def get_users():
        all_users = list(users.find({}, {'_id': 0}))
        return jsonify(all_users)

class EventManagement:
    @staticmethod
    @api.route('/add_event', methods=['POST'])
    def add_event():
        event_data = request.json
        events.insert_one(event_data)
        return jsonify({"message": "Event added successfully!"})

    @staticmethod
    @api.route('/get_events', methods=['GET'])
    def get_events():
        all_events = list(events.find({}, {'_id': 0}))
        return jsonify(all_events)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
