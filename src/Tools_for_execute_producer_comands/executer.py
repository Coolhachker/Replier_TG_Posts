from src.rabbitmq_tools.producer_commands import Commands
from src.Tools_for_execute_producer_comands.start_parser import start_parser
from src.Tools_for_execute_producer_comands.stop_parser import stop_parser


def execute_producer_commands(command: str):
    if command == Commands.TURN_ON_COMMAND:
        return start_parser()
    elif command == Commands.TURN_OFF_COMMAND:
        return stop_parser()
