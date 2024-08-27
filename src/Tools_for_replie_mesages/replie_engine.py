import asyncio
import logging
import re
from asyncio import Task
from telethon import TelegramClient
from src.databases.mongodb import client_mongodb
from src.exceptions.castom_exceptions import Exceptions
from typing import Union
from datetime import datetime
from typing import List, Tuple
from src.Tools_for_replie_mesages.processing_posts import processing
from src.Tools_for_replie_mesages.check_a_post_on_overlap_in_channel_to import check_post
from src.rabbitmq_tools.publish_a_message import publisher
from src.rabbitmq_tools.queue_dataclass import Queue
from src.Tools_for_replie_mesages.commands_for_tasks import CommandsForTask
from src.rabbitmq_tools.producer_commands import Commands
from src.Tools_for_replie_mesages.check_on_tasks import check_on_tasks
logger = logging.getLogger()
#TODO: 1. сделать чек работы парсера по конкретным каналам


class ReplierEngine:
    """
    Класс, которой нужен для работы механизма пересылки постов с каналов. В нем рассматриваются методы отправки,
    получения и обработки постов.
    """
    def __init__(self, api_id: int, api_hash: str):
        self.client_session = TelegramClient('session', api_id, api_hash)
        self.channels_from_get_the_posts = client_mongodb.get_channels_url('from')
        self.channels_to_posts_the_posts = client_mongodb.get_channels_url('to')
        self.task_names: List[str] = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['task_names']

    async def parser_conductor(self):
        while True:
            command = client_mongodb.get_data_from_entry_in_parser_commands('command')
            if command is None:
                await asyncio.sleep(1)
            elif command == Commands.TURN_ON_COMMAND:
                await asyncio.create_task(self.command_turn_on_parser())
            elif command == CommandsForTask.stop_task:
                self.command_stop_task(command)
            elif command == Commands.CHECK_PARSER_COMMAND:
                client_mongodb.set_status_of_work_in_parser_commands(self.command_check_parser())
                client_mongodb.set_command_in_parser_commands(None)

    @staticmethod
    def central_processing_of_commands_to_task(command: str, task_name: str):
        if command == CommandsForTask.stop_task:
            logger.info(f'Остановка таска: {task_name}')
            task_objects = asyncio.all_tasks()
            task = [task for task in task_objects if task.get_name() == task_name][0]
            task.cancel()

    async def central_processing_of_register_tasks(self):
        """
        Центральный процесс регистрации новых тасков, вызывается извне.
        :return:
        """
        self.create_a_task_names()
        list_of_tasks = self.create_tasks_for_replies()
        logger.info(f'Таски для работы: {list_of_tasks}')
        return list_of_tasks

    @staticmethod
    async def center_of_start_tasks(tasks: List[Task]):
        await asyncio.gather(*tasks)

    async def central_processing_of_task(self, channel_to_post: str, channel_from_to_get_post: str):
        """
        Центральный процесс работы таска, он координирует работу методов по работе с постами.
        :param channel_to_post: канал, куда сбывать посты
        :param channel_from_to_get_post: канал, откуда брать посты
        :return:
        """
        task = asyncio.current_task()
        task_name = task.get_name()
        while True:
            try:
                # получаю динамически конфиги
                data_from_configs_of_channels_from_get_posts = client_mongodb.get_config_of_channel(channel_from_to_get_post, 'from')
                data_from_configs_of_channels_to_post_posts = client_mongodb.get_config_of_channel(channel_to_post, 'to')

                upper_datetime_limit, lower_datetime_limit, video_or_photo, morning_post = self.unpack_config_with_key_FROM(data_from_configs_of_channels_from_get_posts)
                emoji, periodicity = self.unpack_config_with_key_TO(data_from_configs_of_channels_to_post_posts)

                id_offset = client_mongodb.get_entry(client_mongodb.collection_for_id_offsets, 'task_name', task_name)['id_offset']
                post = await self.get_post_from_channel(channel_from_to_get_post, message_offset_id=id_offset, offset_date=upper_datetime_limit, reverse=True)
                logger.debug(post)

                #обновляю id_offset в mongodb
                client_mongodb.add_data_in_entry(client_mongodb.collection_for_id_offsets, 'id_offset', post.id, 'task_name', task_name)

                await check_post(post, self.client_session, channel_to_post)

                #обработка поста
                data_for_send_in_channels = await processing(self.client_session, post, video_or_photo, channel_to_post, emoji, lower_datetime_limit, morning_post)

                logger.debug(data_for_send_in_channels)
                await self.send_post_in_channel(channel_to_post, data_for_send_in_channels)
                await asyncio.sleep(periodicity)
            except Exceptions.ExceptionOnUnsuitablePost as _ex:
                logger.error('Поймал некритичную ошибку: ', exc_info=_ex)
                continue
            except Exceptions.ExceptionOnDateOfPost as _ex:
                logger.info('Таск отработал свое время')
                break
            except Exception as _ex:
                logger.critical('Получил критическую ошибку: ', exc_info=_ex)

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
        logger.info('Создание имен тасков')
        for channel_to in self.channels_to_posts_the_posts:
            for channel_from in self.channels_from_get_the_posts:
                if f'{channel_from}-{channel_to}' not in self.task_names:
                    client_mongodb.add_data_in_entry(client_mongodb.collection_for_parser_configs, 'task_names', f'{channel_from}-{channel_to}', 'uniq_key', client_mongodb.uniq_key)
                else:
                    continue
        else:
            self.task_names = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['task_names']

    def create_tasks_for_replies(self) -> List[Task]:
        """
        Создание тасков.
        :return: возвращает список тасков с именами.
        """
        tasks_running = [task.get_name() for task in asyncio.all_tasks() if task.done() is False]
        tasks_waiting: list = []

        for task in self.task_names:
            if task not in tasks_running:
                channel_from, channel_to = task.split('-')[0], task.split('-')[1]
                task_for_replier = asyncio.create_task(self.central_processing_of_task(channel_to, channel_from), name=task)
                task_for_replier.add_done_callback(callback_of_work_task)
                tasks_waiting.append(task_for_replier)
                client_mongodb.register_entry_in_collection_for_id_offsets(task)

        logger.info('Создал таски для пересылки сообщений')
        return tasks_waiting

    @staticmethod
    def unpack_config_with_key_FROM(config) -> Tuple[datetime, float, str, bool]:
        upper_datetime_limit: datetime = datetime.strptime(config['time_from'], '%Y-%m-%d')
        lower_datetime_limit: float = datetime.strptime(config['time_to'], '%Y-%m-%d').timestamp()

        video_or_photo: str = config['video_or_photo']
        morning_post: bool = bool(config['morning_post'])

        return upper_datetime_limit, lower_datetime_limit, video_or_photo, morning_post

    @staticmethod
    def unpack_config_with_key_TO(config) -> Tuple[str, int]:
        emoji: str = config['emoji']
        periodicity: int = config['periodicity']

        return emoji, periodicity

    def command_stop_task(self, command):
        client_mongodb.set_status_of_work_in_parser_commands('working')

        task_name = client_mongodb.get_data_from_entry_in_parser_commands('task_name')
        self.central_processing_of_commands_to_task(command, task_name)

        client_mongodb.set_status_of_work_in_parser_commands(None)
        client_mongodb.set_command_in_parser_commands(None)

    async def command_turn_on_parser(self):
        task_for_register_a_tasks = asyncio.create_task(self.central_processing_of_register_tasks())
        await task_for_register_a_tasks

        asyncio.create_task(self.center_of_start_tasks(task_for_register_a_tasks.result()))
        client_mongodb.set_command_in_parser_commands(None)

    @staticmethod
    def command_check_parser():
        channels_to_post_the_posts = client_mongodb.get_channels_url('to')
        string_for_send_to_user: str = ''
        running_tasks = [task.get_name() for task in asyncio.all_tasks()]
        for channel in channels_to_post_the_posts:
            string_for_send_to_user += channel + ' ' + '->' + ' '
            for task in running_tasks:
                if re.search(channel, task):
                    string_for_send_to_user += '✅︎ Работает\n'
                    break
            else:
                string_for_send_to_user += '❌️ Не работает\n'
        return string_for_send_to_user


def callback_of_work_task(task: asyncio.Task):
    task_name = task.get_name()
    publisher.publish(f'[INFO]: Канал - {task_name.split("-")[1]} получил все посты с датафрейма\n с канала - {task_name.split("-")[0]}.\nИли один из каналов был удален.', Queue.callback_queue)


replier_engine = ReplierEngine(19567654, 'gkadnfnsdkbd')
