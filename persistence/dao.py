import datetime
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://root:root@event-mgmt.3fujjxh.mongodb.net/?retryWrites=true&w=majority&appName=event-mgmt")
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

class InvalidUsernameError(Exception):
    def __init__(self, username):
        super().__init__(f"The username '{username}' is invalid.")

class UserDao:

    def getUser(self, username):
        return users.find_one({'userid': username})

    def createUser(self, user):
        return users.insert_one(user.to_dict())

    def getAllUsers(self):
        return list(users.find({}, {'_id': 0}))

    def getLastTimeStamp(self, username):
        user = self.getUser(username)

        if not user:
            return None
        return user["last_notfication_time"]

    def getUserGenres(self, username):
        user = self.getUser(username)
        if not user:
            return None
        return user["genres"]

    def upDateLastTimeStamp(self, username):
        # Define the filter to identify the document to update
        filter_criteria = {'userid': username}

        # Define the update operation
        update_operation = {
            "$set": {
                "last_notfication_time": datetime.datetime.now()  # Replace with the new value for the field
            }
        }
        users.update_one(filter_criteria, update_operation)

    def userRegister(self, dto):
        users.update_one(
            {"userid": dto["user_id"]},
            {"$push": {"registered_events": dto["registered_events"]}}
        )

    def userUnregister(self, dto):
        users.update_one(
            {"userid": dto["user_id"]},
            {"$pull": {"registered_events": dto["registered_events"]}}
        )

class EventDao:
    def getAllEvents(self):
        print("///////////////////////////////inside get all events^^^^^^^^^^^^^")

        return events.find({}, {'_id': 0}).sort("create_datetime", -1)

    def getEventsByUser(self, dto):
        print("############################## inside get events by user &&&&&&&&&&")
        return events.find({"createdBy": dto["userid"]}, {'_id': 0}).sort("create_datetime", -1)

    def getEventByName(self, dto):
        return events.find_one({"event_name": dto["event_id"]})

    def createEvent(self, event_data):
        print("66666666666666event time: ", )
        events.insert_one(event_data)

    def getNotifications(self, data):
        # Retrieve entries with create_datetime greater than query_time
        user_dao = UserDao()
        last_notification_time = user_dao.getLastTimeStamp(data["userid"])
        print("777777777777777777777777777777777777777777777777777777")
        print("last_notification_time", last_notification_time)
        user_genres = user_dao.getUserGenres(data["userid"])
        print("user_genres", user_genres)
        if not last_notification_time or not user_genres: raise InvalidUsernameError(data["userid"])
        return events.find({"create_datetime": {"$gt": last_notification_time},
                                    "genre": {"$in": user_genres}}, {"_id": 0}).sort("create_datetime", -1)

    def decreaseAvailibility(self, dto):
        filtervar = {'event_name': dto["event_id"]}
        update = {'$inc': {'available_capacity': -1}}

        return events.update_one(filtervar, update)

    def increaseAvailibility(self, dto):
        filtervar = {'event_name': dto["event_id"]}
        update = {'$inc': {'available_capacity': 1}}
        return events.update_one(filtervar, update)