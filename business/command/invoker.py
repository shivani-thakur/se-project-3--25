
from command.command import CreateEventCommand, RegisterEventCommand, GetEventsCommand, GetNotificationCommand


class CommandInvoker:
    def __init__(self, events_collection, users_collection):
        self.commands = {
            "create_event": CreateEventCommand(events_collection, users_collection),
            "register_event": RegisterEventCommand(),
            "get_events": GetEventsCommand(events_collection),
            "get_notifications" : GetNotificationCommand(users_collection)
        }
    # def set_command(self, command):
    #     self.command = command

    def invokeCommand(self, command_name, dto):
        command = self.commands.get(command_name)
        if command:
            return command.execute(dto)
        else:
            return "Invalid Command"