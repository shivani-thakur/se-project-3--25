from abc import ABC, abstractmethod

class CommandInterface(ABC):
    @abstractmethod
    def execute(self):
        pass

class CreateEventCommand(CommandInterface):
    # def __init__(self, dto):
    #     self.dto = dto

    def execute(self, dto):
        # logic to add event to db
        # add observer pattern to notify all users who are interested in this event_type about the event 
        pass
    
class RegisterEventCommand(CommandInterface):
    # def __init__(self, dto):
    #     self.dto = dto

    def execute(self, dto):
        # logic to register user to event
        pass
