from abc import ABC, abstractmethod
import datetime

from flask import jsonify

from persistence.dao import EventDao, UserDao, InvalidUsernameError


# from persistence.dao import EventDao


class CommandInterface(ABC):
    @abstractmethod
    def execute(self, data):
        pass


class CreateEventCommand(CommandInterface):

    def execute(self, event_data):
        if not all(key in event_data for key in
                   ["event_name", "location", "date", "genre", "description", "max_capacity", "create_datetime",
                    "createdBy"]):
            return jsonify({"message": "Missing fields in event data"}), 400

        event_data["create_datetime"] = datetime.datetime.now()
        event_dao = EventDao()
        event_dao.createEvent(event_data)
        # self.events.insert_one(dto)

        return jsonify({"message": "Event created successfully!"}), 201


class RegisterEventCommand(CommandInterface):
    # def __init__(self, events_collection, users_collection):
    #     self.events = events_collection
    #     self.users = users_collection

    def execute(self, dto):
        if not all(key in dto for key in ["event_id", "user_id"]):
            return jsonify({"message": "Missing fields in registration data"}), 400

        event_dao = EventDao()
        event = event_dao.getEventByName(dto)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        user_dao = UserDao()
        user = user_dao.getUser(dto["user_id"])
        if not user:
            return jsonify({"message": "User not found"}), 404

        if any(event["event_name"] == registered_event['event_name'] for registered_event in user.get("registered_events", [])):
            print("here")
            return jsonify({"message": "User already registered for this event"}), 409

        if event['available_capacity'] == 0:
            return jsonify({"message": "Event is full"}), 409

        filtervar = {'event_name': dto["event_id"]}
        update = {'$inc': {'available_capacity': -1}}

        result = event_dao.decreaseAvailibility(dto)
        if result.modified_count == 0:
            return jsonify({"message": "Event is full or not found"}), 400

        dto["registered_events"] = event
        user_dao.userRegister(dto)
        # self.users.update_one(
        #     {"userid": dto["user_id"]},
        #     {"$push": {"registered_events": event}}
        # )

        return jsonify({"message": "Successfully registered for the event"}), 200


class UnregisterEventCommand(CommandInterface):
    # def __init__(self, events_collection, users_collection):
    #     self.events = events_collection
    #     self.users = users_collection

    def execute(self, dto):
        if not all(key in dto for key in ["event_id", "user_id"]):
            return jsonify({"message": "Missing fields in registration data"}), 400

        # event = self.events.find_one({"event_name": dto["event_id"]})
        event_dao = EventDao()
        event = event_dao.getEventByName(dto)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        # user = self.users.find_one({"userid": dto["user_id"]})
        user_dao = UserDao()
        user = user_dao.getUser(dto["user_id"])
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        if any(event["event_name"] == registered_event['event_name'] for registered_event in user.get("registered_events", [])):        
            # filtervar = {'event_name': dto["event_id"]}
            # update = {'$inc': {'available_capacity': 1}}
            # result = self.events.update_one(filtervar, update)
            dto["registered_events"] = event
            event_dao.increaseAvailibility(dto)

            user_dao.userUnregister(dto)
            # self.users.update_one(
            #     {"userid": dto["user_id"]},
            #     {"$pull": {"registered_events": event}}
            # )
            return jsonify({"message": "Successfully unregistered from the event"}), 200
        else:
            return jsonify({"message": "User is not registered for the event"}), 409



class GetEventsCommand(CommandInterface):

    def execute(self, dto=None):
        # If a DTO is provided and contains a 'userID', filter events by userID

        event_dao = EventDao()
        if dto and "userid" in dto:
            events_cursor = event_dao.getEventsByUser(dto)
        else:
            events_cursor = event_dao.getAllEvents()
        
        events_list = list(events_cursor)
        print("888888888888888888888888888888", events_list)
        return jsonify(events_list), 200

class GetNotificationsCommand(CommandInterface):

    def execute(self, data):
        # user_dao = UserDao()
        event_dao = EventDao()
        user_dao = UserDao()
        try:
            events_cursor = event_dao.getNotifications(data)
            if not events_cursor: events_list = []
            else: events_list = list(events_cursor)
            print("9999999999999999999999999999", events_list)

            user_dao.upDateLastTimeStamp(data["userid"])

            return jsonify(events_list), 200
        except InvalidUsernameError as e:
            # print("InvalidUsernameError:", e)
            return jsonify({"message": str(e)})
        # if not events_cursor:
        #     pass


