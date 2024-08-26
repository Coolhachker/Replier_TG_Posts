from src.rabbitmq_tools.producer_commands import Commands
from src.Tools_for_execute_producer_comands.start_parser import start_parser
from src.Tools_for_execute_producer_comands.stop_parser import stop_parser
from src.Tools_for_execute_producer_comands.check_parser import check_parser
from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask
from typing import Optional
from src.Tools_for_execute_producer_comands.stop_task import stop_task


def execute_producer_commands(command: str, dict_of_data: Optional[dict] = None):
    if command == Commands.TURN_ON_COMMAND:
        return start_parser()
    elif command == Commands.TURN_OFF_COMMAND:
        return stop_parser()
    elif command == Commands.CHECK_PARSER_COMMAND:
        return check_parser()
    elif command == CommandsForTask.stop_task:
        return stop_task(dict_of_data)
