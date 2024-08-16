import asyncio

from telethon import TelegramClient
from telethon.types import Message
from telethon.types import InputMessagesFilterVideo
from functools import lru_cache
from typing import List, Union
from src.exceptions.castom_exceptions import Exceptions


async def check_post(post: Message, client_session: TelegramClient, channel_to_post_posts: str) -> Union[None, bool]:
    list_of_bytes_string = await asyncio.create_task(get_posts_from_channel_to_posts(channel_to_post_posts, client_session))
    if post.media.document.thumbs[0].bytes[:20] in list_of_bytes_string:
        raise Exceptions.ExceptionOnUnsuitablePost('Данный пост уже существует в канале')
    else:
        return True


@lru_cache(maxsize=128)
async def get_posts_from_channel_to_posts(channel: str, client_session: TelegramClient) -> List[bytes]:
    posts: List[bytes] = []
    for obj in await client_session.get_messages(channel, limit=50):
        obj: Message
        try:
            posts.append(obj.media.document.thumbs[0].bytes[:20])
        except:
            pass
    return posts

