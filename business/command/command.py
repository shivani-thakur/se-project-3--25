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
    # def __init__(self, dto):
    #     self.dto = dto

    def execute(self, dto):
        # logic to register user to event
        pass


class GetEventsCommand(CommandInterface):
    def __init__(self, events_collection):
        self.events = events_collection

    def execute(self, dto=None):
        # If a DTO is provided and contains a 'genre', filter events by genre
        if dto and "genre" in dto:
            events_cursor = self.events.find({"genre": dto["genre"]}, {'_id': 0})
        else:
            events_cursor = self.events.find({}, {'_id': 0})
        
        events_list = list(events_cursor)
        return jsonify(events_list), 200