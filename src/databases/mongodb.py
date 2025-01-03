from pymongo import MongoClient
from pymongo.collection import Collection
from src.exceptions.castom_exceptions import Exceptions
from typing import Union
from typing import Any
from src.tools_for_tg_bot.Configs.hosts import Hosts
# Образец коллекции "collection_for_parser_configs"
# {
#     "from": [
#         {
#             "https://t.me/video_smeshnye": {
#                 "time_from": "2023-08-27",
#                 "time_to": "2023-09-27",
#                 "video_or_photo": "video",
#                 "morning_post": "False"
#             }
#         }
#     ],
#     "to": [
#         {
#             "https://t.me/manda9ine": {
#                 "emoji": "🍊",
#                 "periodicity": 5400
#             }
#         }
#     ],
#     "token": "",
#     "api_id": 19567654,
#     "api_hash": "7ec7d44a4889e041dd667dc760b323e1"
# }


class MongoDBClient:
    def __init__(self):
        self.connection_string = f'mongodb://{Hosts.mongodb}:27017/'
        self.client = MongoClient(self.connection_string)
        self.uniq_key = 1234567890
        self.collection_for_parser_configs = self.client['replies_config_collection']['collection_for_parser_configs']
        self.collection_for_bot_configs = self.client['replies_config_collection']['collection_for_bot_configs']
        self.collection_for_id_offsets = self.client['replies_config_collection']['collection_for_id_offsets']
        self.collection_for_parser_commands = self.client['replies_config_collection']['collection_for_parser_commands']

        self.register_entry_channels_config()
        self.set_command_entry()

    def register_entry_channels_config(self):
        data = {
            'uniq_key': self.uniq_key,
            'from': [],
            'to': [],
            'stop_words': ['👇👇👇', '👇', 'Подробности', 'НОВОСТИ С ФРОНТА', 'СВО', 'теперь в Telegram', 'Жуткая статистика', 'переплачиваете',
                           'Хватит переплачивать', '@', 'Читать далее', 'Фулл', 'Видео без цензуры', 'Прямая трансляция'],
            'task_names': [],
            'status_check': '',
            'pid_of_parser': None
        }

        if self.collection_for_parser_configs.find_one({'uniq_key': self.uniq_key}) is None:
            self.collection_for_parser_configs.insert_one(data)
        else:
            pass

    def register_entry_in_collection_for_id_offsets(self, task_name):
        data = {
            'task_name': task_name,
            'id_offset': 0
        }

        if self.collection_for_id_offsets.find_one({'task_name': task_name}) is None:
            self.collection_for_id_offsets.insert_one(data)
        else:
            pass

    def add_data_in_entry(self, collection: Collection, key: str, data: Any, uniq_key: str, uniq_value: Union[str, int], update_data_in_entry: bool = False):
        entry = self.get_entry(collection, uniq_key, uniq_value)
        data_from_db = entry[key]
        if type(data_from_db) is list:
            if update_data_in_entry is False:
                data_from_db.append(data)
            else:
                data_from_db = data
        else:
            data_from_db = data

        collection.update_one({uniq_key: uniq_value}, {'$set': {key: data_from_db}})

    @staticmethod
    def get_entry(collection: Collection, uniq_key: str, uniq_value: Union[str, int]):
        return collection.find_one({uniq_key: uniq_value})

    def delete_data_from_entry_in_collection_for_parser_configs(self, direction: str, channel: str) -> None:
        entry = self.get_entry(self.collection_for_parser_configs, 'uniq_key', self.uniq_key)
        data_from_db: list = entry[direction]
        channels_in_entity = [key for obj in data_from_db for key in obj.keys()]
        if channel in channels_in_entity:
            del data_from_db[channels_in_entity.index(channel)]
            client_mongodb.collection_for_parser_configs.update_one({'uniq_key': self.uniq_key}, {'$set': {direction: data_from_db}})
        else:
            raise Exceptions.ExceptionOnUnFoundChannelInDb(f'Не найден канал: {channel} в записи с ключом: {direction}')

    def update_data_in_entity_in_collection_for_parser_configs(self, direction: str, channel: str, data: dict) -> None:
        try:
            self.delete_data_from_entry_in_collection_for_parser_configs(direction, channel)
            self.add_data_in_entry(self.collection_for_parser_configs, direction, data, 'uniq_key', self.uniq_key)
        except Exceptions.ExceptionOnUnFoundChannelInDb:
            self.add_data_in_entry(self.collection_for_parser_configs, direction, data, 'uniq_key', self.uniq_key)

    def get_channels_url(self, direction: str) -> list:
        entry = self.get_entry(self.collection_for_parser_configs, 'uniq_key', self.uniq_key)
        data_from_db = entry[direction]
        return [key for obj in data_from_db for key in obj.keys()] if len(data_from_db) != 0 else []

    def get_emoji(self, channel_url: str) -> str:
        data_from_db = self.get_entry(self.collection_for_parser_configs, 'uniq_key', self.uniq_key)['to']
        for element in data_from_db:
            return element[channel_url]['emoji']

    def get_config_of_channel(self, channel: str, direction: str, with_channel: bool = False) -> dict:
        entry = self.get_entry(self.collection_for_parser_configs, 'uniq_key', self.uniq_key)[direction]
        index_channel = [key for obj in entry for key in obj.keys()].index(channel)
        return entry[index_channel][channel] if with_channel is False else entry[index_channel]

    @staticmethod
    def delete_entry(collection: Collection, uniq_key: str, uniq_value: Union[str, int]):
        collection.delete_one({uniq_key: uniq_value})

    def zeroing_offset_id(self, task_name):
        self.add_data_in_entry(client_mongodb.collection_for_id_offsets, 'id_offset', 0, 'task_name', task_name)

    def get_status_of_parser(self):
        status = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['status_check']
        return status

    def update_status_of_parser(self, status):
        self.add_data_in_entry(self.collection_for_parser_configs, 'status_check', status, 'uniq_key', self.uniq_key)

    def update_pid_of_parser(self, process_parser):
        self.add_data_in_entry(self.collection_for_parser_configs, 'pid_of_parser', process_parser, 'uniq_key', self.uniq_key)

    def set_command_entry(self):
        data = {
            'uniq_key': self.uniq_key,
            'command': None,
            'task_name': None,
            'status_of_work': None
        }
        if self.collection_for_parser_commands.find_one({'uniq_key': self.uniq_key}) is None:
            self.collection_for_parser_commands.insert_one(data)
        else:
            pass

    def set_command_in_parser_commands(self, command: Union[str, None]):
        self.add_data_in_entry(self.collection_for_parser_commands, 'command', command, 'uniq_key', self.uniq_key)

    def set_task_name_in_parser_commands(self, task_name: str):
        self.add_data_in_entry(self.collection_for_parser_commands, 'task_name', task_name, 'uniq_key', self.uniq_key)

    def set_status_of_work_in_parser_commands(self, status: Union[str, None]):
        self.add_data_in_entry(self.collection_for_parser_commands, 'status_of_work', status, 'uniq_key', self.uniq_key)

    def get_data_from_entry_in_parser_commands(self, key: str):
        entry = self.get_entry(self.collection_for_parser_commands, 'uniq_key', client_mongodb.uniq_key)
        return entry[key]

    def reconnect(self):
        self.client = MongoClient(self.connection_string)


client_mongodb = MongoDBClient()