from telethon import TelegramClient
from telethon.types import Message
from src.databases.mongodb import client_mongodb
from typing import Union
from datetime import datetime


class ReplierEngine:
    def __init__(self, api_id: int, api_hash: str):
        self.client_session = TelegramClient('session', api_id, api_hash)
        self.client_session.start()
        self.channels_from_get_the_posts = client_mongodb.get_channels_url('from')
        self.channels_to_posts_the_posts = client_mongodb.get_channels_url('to')

    async def send_post_in_channel(self, channel_to_post: str, data_for_post: dict) -> None:
        await self.client_session.send_message(channel_to_post, **data_for_post)

    async def get_post_from_channel(self, channel_from_to_get_post: str, offset_date: Union[datetime, None] = None, reverse=False) -> Message:
        post = await self.client_session.get_messages(channel_from_to_get_post, offset_date=offset_date, reverse=reverse)
        return post

