import json
from abc import ABC, abstractmethod
from flask import jsonify
from kafka import KafkaProducer, KafkaConsumer


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

        # Define Kafka bootstrap servers
        bootstrap_servers = 'localhost:9092'

        # Kafka producer configuration
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
            # Add more Kafka producer configuration parameters as needed
        )

        # Publish the JSON-formatted message
        message = {
            "event_name": dto['event_name'],
            "location": dto['location'],
            "date": dto['date'],
            "genre": dto['genre'],
            "description": dto['description'],
            "max_capacity": dto['max_capacity'],
            "create_datetime": dto['create_datetime'],
            "createdBy": dto['createdBy']
        }

        # Serialize the message to JSON format
        json_message = json.dumps(message)
        producer.send(dto['genre'], json_message)

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


class GetNotificationCommand(CommandInterface):
    def __init__(self, users_collection):
        self.users = users_collection

    def execute(self, username=None):
        bootstrap_servers = 'localhost:9092'

        # If a DTO is provided and contains a 'genre', filter events by genre
        # if dto and "genre" in dto:
        #     events_cursor = self.events.find({"genre": dto["genre"]}, {'_id': 0})
        # else:
        #     events_cursor = self.events.find({}, {'_id': 0})

        # topic = self.users.find({"userid":username})

        # print("Users type is ",type(self.users))
        # print("Users is\n", self.users)

        user = self.users.find_one({"userid": username})

        # Check if the user exists
        topic=None
        if user:
            # Access the 'genre' field of the user
            print("Found user", user)
            topic = user.get('genres')[0]
            print("User's genre is:", topic)
        else:
            print("User not found.")

        if not topic:
            return None, 200

        consumer = KafkaConsumer(
            topic,
            group_id = username,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',  # Start consuming from the latest offset
            enable_auto_commit=True,  # Disable auto-commit of offsets
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        retval = []
        print("Got consumer", consumer)

        # Poll for messages with a timeout of 1000 milliseconds (1 second)
        messages = consumer.poll(timeout_ms=1000)

        # Iterate over the messages received within the timeout period
        for topic_partition, records in messages.items():
            for record in records:
                # Append the value of each message to the retval list
                retval.append(record.value)
                print("Got retval", retval)
                print("Message is", record)

        consumer.close()
        return jsonify(retval), 200
