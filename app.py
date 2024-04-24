# from business.command.invoker import CommandInvoker
import datetime

from business.dto.UserDto import UserDto
from business.command.invoker import CommandInvoker
from flask import Flask, jsonify, request, Blueprint
# from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from persistence.dao import UserDao

app = Flask(__name__)
CORS(app)
api = Blueprint('api', __name__)


class UserManagement:
    @staticmethod
    @api.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        print("Retrieved username is", username)
        # user = users.find_one({'userid': username})
        user_Dao = UserDao()
        user = user_Dao.getUser(username)
        print("user retrieved", user)
        print("Retrieved password is", user['password'])

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


        user_Dao = UserDao()
        existing_user = user_Dao.getUser(username)

        # existing_user = users.find_one({'userid': username})

        if existing_user:
            return jsonify({"message": "User already exists"}), 401

        hashed_password = generate_password_hash(password)

        user_dto = UserDto()
        user_dto.username = username
        user_dto.hashed_password = hashed_password
        user_dto.genres = genres
        user_dto.last_notfication_time = datetime.datetime.now()

        print("0000000000000000000000000signup time:", user_dto.last_notfication_time)
        # user = {
        #     'userid': username,
        #     'password': hashed_password,
        #     'genres': genres,
        #     'last_notfication_time': lasttime
        # }

        # users.insert_one(user)
        user_Dao.createUser(user_dto)

        return jsonify({"message": "User added successfully!"}), 200

    @staticmethod
    @api.route('/get_users', methods=['GET'])
    def get_users():
        user_dao = UserDao()
        all_users = user_dao.getAllUsers()
        return jsonify(all_users)


class EventManagement:
    command_invoker = CommandInvoker()

    @staticmethod
    @api.route('/add_event', methods=['POST'])
    def add_event():
        # command_invoker = CommandInvoker(events, users)
        event_dto = request.json
        return EventManagement.command_invoker.invokeCommand("create_event", event_dto)

    @staticmethod
    @api.route('/register', methods=['POST'])
    def register_event():
        # command_invoker = CommandInvoker(events, users)
        register_dto = request.json
        return EventManagement.command_invoker.invokeCommand("register_event", register_dto)

    @staticmethod
    @api.route('/get_events', methods=['GET'])
    def get_events():
        # command_invoker = CommandInvoker()
        username = request.args.get('username')
        dto = {'userid': username} if username else None
        return EventManagement.command_invoker.invokeCommand("get_events", dto)

    @staticmethod
    @api.route('/get_notifications', methods=['GET'])
    def get_notifications():
        username = request.args.get('username')
        if not username: jsonify({"message": "provide username"}), 401
        data = {'userid': username}
        events_list = EventManagement.command_invoker.invokeCommand("get_notifications", data)
        # if not events_list: return jsonify({"message": "Invalid username"}), 401
        return events_list

    @staticmethod
    @api.route('/unregister_event', methods=['POST'])
    def unregister_event():
        # command_invoker = CommandInvoker(events, users)
        unregister_dto = request.json
        return EventManagement.command_invoker.invokeCommand("unregister_event", unregister_dto)


app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
