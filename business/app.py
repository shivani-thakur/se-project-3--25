# from business.command.invoker import CommandInvoker
from command.invoker import CommandInvoker
from flask import Flask, jsonify, request, Blueprint
from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import json


app = Flask(__name__)
CORS(app)
api = Blueprint('api', __name__)

client = MongoClient("mongodb+srv://root:root@event-mgmt.3fujjxh.mongodb.net/?retryWrites=true&w=majority&appName=event-mgmt")
db = client["event-mgmt"]

users = db['users']
user_schema = {
    "userid": str,
    "password": str,
    "genre": [str],
    "registered_events": [dict],
    "last_notfication_time": datetime.datetime
}

events = db['events']
event_schema = {
    "event_name": str,
    "location": str,
    "date": str,
    "genre": str,
    "description": str,
    "max_capacity": int,
    "available_capacity": int,
    "create_datetime": datetime.datetime,
    "createdBy": str
}

# Define Kafka bootstrap servers
bootstrap_servers = 'localhost:9092'

# Define Kafka topics
topics = ["conference", "workshop", "concert", "festival", "tournament"]


# Function to create Kafka topics if they don't exist
def create_topics_if_not_exist():
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    existing_topics = admin_client.list_topics()
    new_topics = [NewTopic(name=topic, num_partitions=1, replication_factor=1) for topic in topics if topic not in existing_topics]
    if new_topics:
        admin_client.create_topics(new_topics=new_topics, validate_only=False)
    admin_client.close()


# # Create Kafka topics
create_topics_if_not_exist()


# Function to list all current topics
def list_topics():
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    topics_metadata = admin_client.list_topics()
    print(topics_metadata)
    admin_client.close()

# List all current topics
# list_topics()


class UserManagement:
    @staticmethod
    @api.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = users.find_one({'userid': username})

        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    
    @staticmethod
    @api.route('/add_user', methods=['POST'])
    def add_user():
        data = request.json
        username = data.get('userid')
        password = data.get('password')
        genres = data.get('genres')
        lasttime = data.get('last_notfication_time')

        existing_user = users.find_one({'userid': username})

        if existing_user:
            return jsonify({"message": "User already exists"}), 401
        
        hashed_password = generate_password_hash(password)

        user = {
            'userid': username,
            'password': hashed_password,
            'genres': genres,
            'last_notfication_time': lasttime
        }

        users.insert_one(user)
        
        return jsonify({"message": "User added successfully!"}), 200

    @staticmethod
    @api.route('/get_users', methods=['GET'])
    def get_users():
        all_users = list(users.find({}, {'_id': 0}))
        return jsonify(all_users)

class EventManagement:
    @staticmethod
    @api.route('/add_event', methods=['POST'])
    def add_event():
        command_invoker = CommandInvoker(events, users)
        event_dto = request.json
        return command_invoker.invokeCommand("create_event", event_dto)
    
    @staticmethod
    @api.route('/register', methods=['POST'])
    def register_event():
        register_dto = request.json
        return CommandInvoker.invokeCommand("register_event", register_dto)

    @staticmethod
    @api.route('/get_events', methods=['GET'])
    def get_events():
        command_invoker = CommandInvoker(events, users)
        genre = request.args.get('genre')
        dto = {'genre': genre} if genre else None
        return command_invoker.invokeCommand("get_events", dto)

    @staticmethod
    @api.route('/get_notifications', methods=['GET'])
    def get_notifications():
        command_invoker = CommandInvoker(events, users)
        username = request.args.get('username')
        return command_invoker.invokeCommand("get_notifications", username)


app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
