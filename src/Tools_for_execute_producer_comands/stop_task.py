import time

from src.Tools_for_replie_mesages.replie_engine import ReplierEngine
from src.databases.vedis_db import db_client
from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask


def stop_task(dict_data: dict):
    task_names = dict_data['task_names']
    try:
        for task_name in task_names:
            db_client.set_object(CommandsForTask.stop_task, db_client.key_command)

            db_client.set_object(task_name, db_client.key_task_name)
            while db_client.get_object(db_client.status) == 'working':
                pass
    except Exception as _ex:
        print(_ex)
        return 'ERROR: не удалось остановить таски'


