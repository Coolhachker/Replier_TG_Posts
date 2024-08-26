import json

from src.databases.mongodb import client_mongodb
from src.rabbitmq_tools.producer_commands import Commands
from src.rabbitmq_tools.producer import producer
import re
from typing import List
from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask
from src.rabbitmq_tools.producer import producer


class Eraser:
    def __init__(self, channel: str, direction: str):
        self.channel = channel
        self.direction = direction

    def start_erase(self):
        if self.check_on_performance():
            task_names: List[str] = [task_name for task_name in client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['task_names'] if re.search(self.channel, task_name)]
            data_for_send = {'command': CommandsForTask.stop_task,
                             'task_names': task_names}

            result = producer.publish(json.dumps(data_for_send), queue=producer.parser_tasks_queue)

        self.delete_the_entry_in_offset_id_collection()
        self.delete_channel_from_task_names()
        self.delete_channel_from_directions()

    def delete_the_entry_in_offset_id_collection(self):
        task_names: List[str] = [task_name for task_name in client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['task_names'] if re.search(self.channel, task_name)]
        for task_name in task_names:
            client_mongodb.delete_entry(client_mongodb.collection_for_id_offsets, 'task_name', task_name)

    def delete_channel_from_directions(self):
        client_mongodb.delete_data_from_entry_in_collection_for_parser_configs(self.direction, self.channel)

    def delete_channel_from_task_names(self):
        task_names: List[str] = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['task_names']
        task_names_buffer = task_names.copy()

        for index, task_name in enumerate(task_names_buffer):
            if re.search(self.channel, task_name):
                del task_names[index]
            else:
                continue

        client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'task_names', task_names, 'uniq_key', client_mongodb.uniq_key, update_data_in_entry=True)

    @staticmethod
    def check_on_performance():
        result = producer.publish(Commands.CHECK_PARSER_COMMAND)
        if re.search('Парсер работает', result):
            return True
        elif re.search('Парсер не работает', result):
            return False