from src.rabbitmq_tools.producer_commands import Commands
from start_parser import start_parser
from stop_parser import stop_parser


def execute_producer_commands(command: str):
    if command == Commands.TURN_ON_COMMAND:
        return start_parser()
    elif command == Commands.TURN_OFF_COMMAND:
        return stop_parser()
