
from command.command import CreateEventCommand, RegisterEventCommand


class CommandInvoker:
    def __init__(self):
        self.commands = {
            "create_event": CreateEventCommand(),
            "register_event": RegisterEventCommand()
        }
    # def set_command(self, command):
    #     self.command = command

    def invokeCommand(self, command_name, dto):
        command = self.commands.get(command_name)
        if command:
            return command.execute(dto)
        else:
            return "Invalid Command"