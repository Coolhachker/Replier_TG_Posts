from src.databases.mongodb import client_mongodb
from telethon.types import Message
from telethon import TelegramClient
import re
from src.exceptions.castom_exceptions import Exceptions
from typing import List


async def processing(client_session: TelegramClient, post: Message, photo_or_video: str, channel_to_post: str) -> dict:
    """
    Основной задачей функции является обработка постов перед их отправкой, а именно
    замена ссылок на новые ссылки, сохранение пути фото/видео, обнаружение спам сообщений
    :param client_session: сессия telethon
    :param post: объект Message
    :param photo_or_video: 'photo' or 'video'
    :param channel_to_post: url ссылка на канал, куда отправлять сообщения
    :return: словарь из данных
    """
    dict_of_data: dict = {}
    mime_type: str = post.media.document.mime_type.split('/')[0]
    message_text: str = post.message
    emoji = client_mongodb.get_emoji(channel_to_post)
    if check_post_on_media(mime_type, photo_or_video) and check_post_on_advert(message_text):
        entity_channel_to_post = await client_session.get_entity(channel_to_post)
        blob = await client_session.download_media(post, bytes)
        file = await client_session.upload_file(blob)
        file.name = mime_type + '.mp4' if photo_or_video == 'video' else mime_type + '.jpg'
        message_text_split = message_text.split('\n')
        message_text = message_text.replace(message_text_split[-1], f'<a href="{channel_to_post}">{entity_channel_to_post.title}{emoji}</a>') if len(message_text_split) > 1 else f'{message_text}\n<a href="{channel_to_post}">{entity_channel_to_post.title}{emoji}</a>'

        dict_of_data['file'] = file
        dict_of_data['message'] = message_text
        dict_of_data['parse_mode'] = 'html'

        return dict_of_data
    else:
        raise Exceptions.ExceptionOnUnsuitablePost('пост либо рекламный / либо не содержит медиа')


def check_post_on_media(mime_type: str, type_of_media: str) -> bool:
    if re.search(type_of_media, mime_type):
        return True
    else:
        return False


def check_post_on_advert(message: str) -> bool:
    stop_words: List[str] = client_mongodb.get_entry(client_mongodb.collection_for_parser_configs, 'uniq_key', client_mongodb.uniq_key)['stop_words']
    for word in stop_words:
        if re.search(word.lower(), message.lower()):
            return False
    return True