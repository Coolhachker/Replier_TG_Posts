from telethon import TelegramClient
from src.databases.mongodb import client_mongodb


class ReplierEngine:
    def __init__(self, api_id: int, api_hash: str):
        self.client_session = TelegramClient('session', api_id, api_hash)
        self.client_session.start()
        self.channels_from_get_the_posts = client_mongodb.get_channels_url('from')
        self.channels_to_posts_the_posts = client_mongodb.get_channels_url('to')

