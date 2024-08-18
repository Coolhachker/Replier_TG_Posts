from pymongo import MongoClient
from pymongo.collection import Collection
from src.exceptions.castom_exceptions import Exceptions
from typing import Union
from functools import lru_cache
from typing import Any
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
        connection_string = 'mongodb://127.0.0.1:27017/'
        self.client = MongoClient(connection_string)
        self.uniq_key = 1234567890
        self.collection_for_parser_configs = self.client['replies_config_collection']['collection_for_parser_configs']
        self.collection_for_bot_configs = self.client['replies_config_collection']['collection_for_bot_configs']
        self.collection_for_id_offsets = self.client['replies_config_collection']['collection_for_id_offsets']

    def register_entry_channels_config(self):
        data = {
            'uniq_key': self.uniq_key,
            'from': [],
            'to': [],
            'stop_words': ['👇👇👇', '👇', 'Подробности', 'НОВОСТИ С ФРОНТА', 'СВО', 'теперь в Telegram', 'Жуткая статистика', 'переплачиваете',
                           'Хватит переплачивать', '@', 'Читать далее', 'Фулл', 'Видео без цензуры', 'Прямая трансляция'],
            'task_names': [],
            'status_check': '',
            'parser_process': None
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

    def add_data_in_entry(self, collection: Collection, key: str, data: Any, uniq_key: str, uniq_value: Union[str, int]):
        entry = self.get_entry(collection, uniq_key, uniq_value)
        data_from_db = entry[key]
        if type(data_from_db) is list:
            data_from_db.append(data)
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

    @lru_cache
    def get_config_of_channel(self, channel: str, direction: str) -> dict:
        entry = self.get_entry(self.collection_for_parser_configs, 'uniq_key', self.uniq_key)[direction]
        index_channel = [key for obj in entry for key in obj.keys()].index(channel)
        return entry[index_channel][channel]

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

    def update_process_parser(self, process_parser):
        self.add_data_in_entry(self.collection_for_parser_configs, 'parser_process', process_parser, 'uniq_key', self.uniq_key)


client_mongodb = MongoDBClient()
