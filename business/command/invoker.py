# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from command import CreateEventCommand, RegisterEventCommand, GetEventsCommand
from business.command.command import CreateEventCommand, RegisterEventCommand, GetEventsCommand, GetNotificationsCommand, UnregisterEventCommand

class CommandInvoker:
    def __init__(self):
        self.commands = {
            "create_event": CreateEventCommand(),
            "register_event": RegisterEventCommand(),
            "get_events": GetEventsCommand(),
            "get_notifications": GetNotificationsCommand(),
            "unregister_event": UnregisterEventCommand()
        }
    # def set_command(self, command):
    #     self.command = command

    def invokeCommand(self, command_name, dto):
        command = self.commands.get(command_name)
        if command:
            return command.execute(dto)
        else:
            return "Invalid Command"