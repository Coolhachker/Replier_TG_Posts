import asyncio
from asyncio import Task
from telethon import TelegramClient
from telethon.types import Message
from src.databases.mongodb import client_mongodb
from typing import Union
from datetime import datetime
from typing import List
#TODO: нужно написать систему динамического обновления переменных, а то бишь сделать постоянный вызов функций для обновления
#   конфигов.


class ReplierEngine:
    def __init__(self, api_id: int, api_hash: str):
        self.client_session = TelegramClient('session', api_id, api_hash)
        self.client_session.start()
        self.channels_from_get_the_posts = client_mongodb.get_channels_url('from')
        self.channels_to_posts_the_posts = client_mongodb.get_channels_url('to')
        self.task_names: List[str] = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs)['tasks_names']

    async def central_processing_of_register_tasks(self):
        self.create_a_task_names()
        await asyncio.gather(*self.create_tasks())

    async def central_processing_of_task(self, channel_to_post: str, channel_from_to_get_post: str):
        id_offset: int = 0
        while True:
            print(self.get_post_from_channel(channel_from_to_get_post))
            break

    async def send_post_in_channel(self, channel_to_post: str, data_for_post: dict) -> None:
        await self.client_session.send_message(channel_to_post, **data_for_post)

    async def get_post_from_channel(self, channel_from_to_get_post: str, offset_date: Union[datetime, None] = None, reverse: bool = False, message_offset_id: int = 0) -> Message:
        await asyncio.sleep(0.2)
        post = await self.client_session.get_messages(channel_from_to_get_post, offset_date=offset_date, reverse=reverse, offset_id=message_offset_id, limit=1)
        return post

    def create_a_task_names(self):
        task_names = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs)['tasks_names']
        for channel_to in self.channels_to_posts_the_posts:
            for channel_from in self.channels_from_get_the_posts:
                if f'{channel_from}-{channel_to}' not in task_names:
                    client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'tasks_names', f'{channel_from}-{channel_to}')
                else:
                    continue
        else:
            self.task_names = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs)['tasks_names']

    def create_tasks(self) -> List[Task]:
        tasks_running = [task.get_name() for task in asyncio.all_tasks() if task.done() is False]
        tasks_waiting: list = []

        for task in self.task_names:
            if task not in tasks_running:
                channel_from, channel_to = task.split('-')[0], task.split('-')[1]
                tasks_waiting.append(asyncio.create_task(self.central_processing_of_task(channel_to, channel_from), name=task))
        return tasks_waiting
