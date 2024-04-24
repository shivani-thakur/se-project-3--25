from abc import ABC, abstractmethod
from flask import jsonify

class CommandInterface(ABC):
    @abstractmethod
    def execute(self):
        pass

class CreateEventCommand(CommandInterface):
    def __init__(self, events_collection, users_collection):
        self.events = events_collection
        self.users = users_collection

    def execute(self, dto):
        if not all(key in dto for key in ["event_name", "location", "date", "genre", "description", "max_capacity", "create_datetime", "createdBy"]):
            return jsonify({"message": "Missing fields in event data"}), 400
        
        self.events.insert_one(dto)

        return jsonify({"message": "Event created successfully!"}), 201
    
class RegisterEventCommand(CommandInterface):
    def __init__(self, events_collection, users_collection):
        self.events = events_collection
        self.users = users_collection

    def execute(self, dto):
        if not all(key in dto for key in ["event_id", "user_id"]):
            return jsonify({"message": "Missing fields in registration data"}), 400

        event = self.events.find_one({"event_name": dto["event_id"]})
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        user = self.users.find_one({"userid": dto["user_id"]})
        if not user:
            return jsonify({"message": "User not found"}), 404

        if any(event["event_name"] == registered_event['event_name'] for registered_event in user.get("registered_events", [])):
            print("here")
            return jsonify({"message": "User already registered for this event"}), 409

        if event['available_capacity'] == 0:
            return jsonify({"message": "Event is full"}), 409

        filtervar = {'event_name': dto["event_id"]}
        update = {'$inc': {'available_capacity': -1}}

        result = self.events.update_one(filtervar, update)
        if result.modified_count == 0:
            return jsonify({"message": "Event is full or not found"}), 400

        self.users.update_one(
            {"userid": dto["user_id"]},
            {"$push": {"registered_events": event}}
        )

        return jsonify({"message": "Successfully registered for the event"}), 200


class UnregisterEventCommand(CommandInterface):
    def __init__(self, events_collection, users_collection):
        self.events = events_collection
        self.users = users_collection

    def execute(self, dto):
        if not all(key in dto for key in ["event_id", "user_id"]):
            return jsonify({"message": "Missing fields in registration data"}), 400
        
        event = self.events.find_one({"event_name": dto["event_id"]})
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        user = self.users.find_one({"userid": dto["user_id"]})
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        if any(event["event_name"] == registered_event['event_name'] for registered_event in user.get("registered_events", [])):        
            filtervar = {'event_name': dto["event_id"]}
            update = {'$inc': {'available_capacity': 1}}
            result = self.events.update_one(filtervar, update)

            self.users.update_one(
                {"userid": dto["user_id"]},
                {"$pull": {"registered_events": event}}
            )
            return jsonify({"message": "Successfully unregistered from the event"}), 200
        else:
            return jsonify({"message": "User is not registered for the event"}), 409



class GetEventsCommand(CommandInterface):
    def __init__(self, events_collection):
        self.events = events_collection

    def execute(self, dto=None):
        if dto and "userid" in dto:
            events_cursor = self.events.find({"createdBy": dto["userid"]}, {'_id': 0}).sort("create_datetime", -1)
        else:
            events_cursor = self.events.find({}, {'_id': 0}).sort("create_datetime", -1)
        
        events_list = list(events_cursor)
        return jsonify(events_list), 200