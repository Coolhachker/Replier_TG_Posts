from src.rabbitmq_tools.producer_commands import Commands
from src.Tools_for_execute_producer_comands.start_parser import start_parser
from src.Tools_for_execute_producer_comands.stop_parser import stop_parser
from src.Tools_for_execute_producer_comands.check_parser import check_parser
from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask
from typing import Optional
from src.Tools_for_execute_producer_comands.stop_task import stop_task
from src.Tools_for_execute_producer_comands.start_task import start_task
import logging
logger = logging.getLogger()


def execute_producer_commands(command: str, dict_of_data: Optional[dict] = None):
    logger.info(f'execute_producer_commands исполняет команду: {command}')
    if command == CommandsForTask.stop_task:
        return stop_task(dict_of_data)
    elif command == CommandsForTask.start_task:
        return start_task(dict_of_data)
    if command == Commands.TURN_ON_COMMAND:
        return start_parser()
    elif command == Commands.TURN_OFF_COMMAND:
        return stop_parser()
    elif command == Commands.CHECK_PARSER_COMMAND or Commands.GET_CHANNELS_COMMAND:
        return check_parser()