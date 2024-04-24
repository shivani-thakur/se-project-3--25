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
    # def __init__(self, dto):
    #     self.dto = dto

    def execute(self, dto):
        # logic to register user to event
        pass


class GetEventsCommand(CommandInterface):

    def execute(self, dto=None):
        # If a DTO is provided and contains a 'userID', filter events by userID

        event_dao = EventDao()
        if dto and "userid" in dto:
            # events_cursor = self.events.find({"createdBy": dto["userid"]}, {'_id': 0})
            events_cursor = event_dao.getEventsByUser(dto)
        else:
            events_cursor = event_dao.getAllEvents()

        # if not events_cursor: return jsonify({"message": "NO NEW NOTIFICATIONS"})

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


