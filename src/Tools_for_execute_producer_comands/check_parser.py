import time
from src.databases.mongodb import client_mongodb
from src.rabbitmq_tools.producer_commands import Commands
import re


def check_parser():
    status_of_parser = client_mongodb.get_status_of_parser()
    client_mongodb.set_command_in_parser_commands(Commands.CHECK_PARSER_COMMAND)
    while True:
        status = client_mongodb.get_data_from_entry_in_parser_commands('status_of_work')
        if re.search('не работает', status_of_parser) or status_of_parser == '':
            return status_of_parser if status_of_parser != '' else 'OK: Парсер не работает'
        if status is None:
            time.sleep(1)
        else:
            status_of_parser += '\n' + status
            break
    client_mongodb.set_status_of_work_in_parser_commands(None)
    return status_of_parser