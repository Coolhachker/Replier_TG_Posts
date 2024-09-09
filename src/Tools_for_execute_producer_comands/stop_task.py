import time
from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask
from src.databases.mongodb import client_mongodb
import logging
logger = logging.getLogger()


def stop_task(dict_data: dict):
    logger.info('Останавливаю таск уровень 1')
    task_names = dict_data['task_names']
    try:
        for task_name in task_names:
            client_mongodb.set_command_in_parser_commands(CommandsForTask.stop_task)
            client_mongodb.set_task_name_in_parser_commands(task_name)
            time.sleep(2)
            while True:
                if client_mongodb.get_data_from_entry_in_parser_commands('status_of_work') == 'working':
                    time.sleep(1)
                else:
                    break
    except Exception as _ex:
        logger.error('Получил ошибку.', exc_info=_ex)
        return 'ERROR: не удалось остановить таски'


