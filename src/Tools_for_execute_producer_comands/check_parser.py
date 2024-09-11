import time
from src.databases.mongodb import client_mongodb
from src.rabbitmq_tools.producer_commands import Commands
import re
import logging
logger = logging.getLogger()


def check_parser():
    status_of_parser = client_mongodb.get_status_of_parser()
    client_mongodb.set_command_in_parser_commands(Commands.CHECK_PARSER_COMMAND)
    count: int = 0
    while True:
        status = client_mongodb.get_data_from_entry_in_parser_commands('status_of_work')
        if (re.search('не работает', status_of_parser) or status_of_parser == '') or (count == 5):
            return 'OK: Парсер не работает'
        if status is None:
            logger.debug(f'Состояние системы: {status}')
            time.sleep(1)
            count += 1
        else:
            status_of_parser += '\n' + status
            break
    client_mongodb.set_status_of_work_in_parser_commands(None)
    return status_of_parser