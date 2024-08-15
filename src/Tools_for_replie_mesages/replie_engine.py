import asyncio
import logging
from asyncio import Task
from telethon import TelegramClient
from src.databases.mongodb import client_mongodb
from src.exceptions.castom_exceptions import Exceptions
from typing import Union
from datetime import datetime
from typing import List
from logging import basicConfig
from processing_posts import processing
#TODO: нужно написать систему динамического обновления переменных, а то бишь сделать постоянный вызов функций для обновления
#   конфигов.
basicConfig(filename='../../data/replier.log', filemode='w', level=logging.DEBUG, format='[%(levelname)s] - %(funcName)s - %(message)s')
logger = logging.getLogger()


class ReplierEngine:
    """
    Класс, которой нужен для работы механизма пересылки постов с каналов. В нем рассматриваются методы отправки,
    получения и обработки постов.
    """
    def __init__(self, api_id: int, api_hash: str):
        self.client_session = TelegramClient('session', api_id, api_hash)
        self.client_session.start()
        self.channels_from_get_the_posts = client_mongodb.get_channels_url('from')
        self.channels_to_posts_the_posts = client_mongodb.get_channels_url('to')
        self.task_names: List[str] = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['task_names']

    async def central_processing_of_register_tasks(self):
        """
        Центральный процесс регистрации новых тасков, вызывается извне.
        :return:
        """
        self.create_a_task_names()
        await asyncio.gather(*self.create_tasks())

    async def central_processing_of_task(self, channel_to_post: str, channel_from_to_get_post: str):
        """
        Центральный процесс работы таска, он координирует работу методов по работе с постами.
        :param channel_to_post: канал, куда сбывать посты
        :param channel_from_to_get_post: канал, откуда брать посты
        :return:
        """
        task_name = asyncio.current_task().get_name()
        while True:
            try:
                id_offset = client_mongodb.get_entry(client_mongodb.collection_for_id_offsets, 'task_name', task_name)['id_offset']
                post = await self.get_post_from_channel(channel_from_to_get_post, message_offset_id=id_offset)
                #обновляю id_offset в mongodb
                client_mongodb.add_data_in_entry(client_mongodb.collection_for_id_offsets, 'id_offset', post.id, 'task_name', task_name)

                data_for_send_in_channels = await processing(self.client_session, post, 'video', channel_to_post)

                logger.debug(post)
                logger.debug(data_for_send_in_channels)
                await self.send_post_in_channel(channel_to_post, data_for_send_in_channels)
                break
            except (Exceptions.ExceptionOnUnsuitablePost, Exception) as _ex:
                logger.error('Поймал ошибку: ', exc_info=_ex)
                continue

    async def send_post_in_channel(self, channel_to_post: str, data_for_post: dict) -> None:
        """
        Метод нужен, чтобы отправлять посты в канал
        :param channel_to_post: канал, куда сбывать сообщения
        :param data_for_post: данные для отправки dict объект
        :return:
        """
        await self.client_session.send_message(channel_to_post, **data_for_post)
        logger.info('Успешная отправка сообщения')

    async def get_post_from_channel(self, channel_from_to_get_post: str, offset_date: Union[datetime, None] = None, reverse: bool = False, message_offset_id: int = 0):
        """
        Метод нужен, чтобы получить один пост с канала
        :param channel_from_to_get_post: канал откуда брать посты
        :param offset_date: смещение по дате
        :param reverse: bool аргумент, который определяет порядок получения постов. Либо сверху вниз, либо сниизу вверх
        :param message_offset_id: смещение по id сообщения
        :return:
        """
        await asyncio.sleep(0.2)
        post = await self.client_session.get_messages(channel_from_to_get_post, offset_date=offset_date, reverse=reverse, offset_id=message_offset_id, limit=1)
        return post[0]

    def create_a_task_names(self):
        """
        Создание имен для тасков.
        :return:
        """
        for channel_to in self.channels_to_posts_the_posts:
            for channel_from in self.channels_from_get_the_posts:
                if f'{channel_from}-{channel_to}' not in self.task_names:
                    client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'task_names', f'{channel_from}-{channel_to}')
                else:
                    continue
        else:
            self.task_names = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['task_names']

    def create_tasks(self) -> List[Task]:
        """
        Создание тасков.
        :return: возвращает список тасков с именами.
        """
        tasks_running = [task.get_name() for task in asyncio.all_tasks() if task.done() is False]
        tasks_waiting: list = []

        for task in self.task_names:
            if task not in tasks_running:
                channel_from, channel_to = task.split('-')[0], task.split('-')[1]
                tasks_waiting.append(asyncio.create_task(self.central_processing_of_task(channel_to, channel_from), name=task))
                client_mongodb.register_entry_in_collection_for_id_offsets(task)
        return tasks_waiting


if __name__ == '__main__':
    replier_engine = ReplierEngine(19567654, 'gkadnfnsdkbd')
    asyncio.get_event_loop().run_until_complete(replier_engine.central_processing_of_register_tasks())
