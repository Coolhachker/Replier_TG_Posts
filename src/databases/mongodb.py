from pymongo import MongoClient
from pymongo.collection import Collection
from src.exceptions.castom_exceptions import Exceptions

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

    def register_entry_channels_config(self):
        data = {
            'uniq_key': self.uniq_key,
            'from': [],
            'to': [],
            'stop_words': ['👇👇👇', '👇', 'Подробности', 'НОВОСТИ С ФРОНТА', 'СВО', 'теперь в Telegram', 'Жуткая статистика', 'переплачиваете',
                           'Хватит переплачивать', '@', 'Читать далее', 'Фулл', 'Видео без цензуры', 'Прямая трансляция']
        }

        if self.collection_for_parser_configs.find_one({'uniq_key': self.uniq_key}) is None:
            self.collection_for_parser_configs.insert_one(data)
        else:
            pass

    def add_data_in_entry(self, collection: Collection, key: str, data: dict):
        entry = self.get_entry(collection)
        data_from_db = entry[key]
        if type(data_from_db) is list:
            data_from_db.append(data)
        else:
            data_from_db = data

        collection.update_one({'uniq_key': self.uniq_key}, {'$set': {'key': data_from_db}})

    def get_entry(self, collection: Collection):
        return collection.find_one({'uniq_key': self.uniq_key})

    def delete_data_from_entry_in_collection_for_parser_configs(self, direction: str, channel: str):
        entry = self.get_entry(self.collection_for_parser_configs)
        data_from_db: list = entry[direction]
        channels_in_entity = [obj.keys() for obj in data_from_db]
        if channel in channels_in_entity:
            del data_from_db[channels_in_entity.index(channel)]
        else:
            raise Exceptions.ExceptionOnUnFoundChannelInDb(f'Не найден канал: {channel} в записи с ключом: {direction}')

    def update_data_in_entity_in_collection_for_parser_configs(self, direction: str, channel: str, data: dict):
        self.delete_data_from_entry_in_collection_for_parser_configs(direction, channel)
        self.add_data_in_entry(self.collection_for_parser_configs, direction, data)

    def get_channels_url(self, direction: str):
        entry = self.get_entry(self.collection_for_parser_configs)
        data_from_db = entry[direction]
        return [obj.keys() for obj in data_from_db] if len(data_from_db) != 0 else []

    def get_emoji(self, channel_url: str):
        data_from_db = self.get_entry(self.collection_for_parser_configs)['to']
        for element in data_from_db:
            if element.keys() == channel_url:
                return element['emoji']


client_mongodb = MongoDBClient()