import time
from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask
from src.databases.mongodb import client_mongodb
import logging
logger = logging.getLogger()


def start_task(dict_data: dict):
    logger.info('Запускаю таск')
    channel = dict_data['channel']
    try:
        client_mongodb.set_command_in_parser_commands(CommandsForTask.start_task)
        client_mongodb.set_task_name_in_parser_commands(channel)
        time.sleep(2)
        while True:
            if client_mongodb.get_data_from_entry_in_parser_commands('status_of_work') == 'working':
                time.sleep(1)
            else:
                break
        return f'Канал {channel} -> ✅︎ работает'
    except Exception as _ex:
        logger.error('Получил ошибку.', exc_info=_ex)
        return 'ERROR: не удалось  таски'
