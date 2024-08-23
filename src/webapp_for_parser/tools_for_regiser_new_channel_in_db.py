from aiogram import Bot
from src.databases.mongodb import client_mongodb
import re

async def register_channel_to_post_the_posts(bot: Bot, chat_id: int, data) -> None:
    assert data['url'] != ''
    assert data['periodic'] != ''
    assert int(data['periodic'])

    url = data['url']
    periodic = int(data['periodic'])
    emoji = data['emoji']

    data_of_channel = {
        url:
            {
                'periodicity': periodic,
                'emoji': emoji
             }
    }

    client_mongodb.register_entry_channels_config()
    client_mongodb.update_data_in_entity_in_collection_for_parser_configs('to', url, data_of_channel)

    await bot.send_message(chat_id, f'✅︎ Добавил в базу данных канал:\n**{url}**', parse_mode='markdown')


async def register_channel_from_get_the_posts(bot: Bot, chat_id: int, data) -> None:
    url = data['url']
    upper_date_limit = data['date_from']
    lower_date_limit = data['date_to']
    video_or_photo = data['video_or_photo']
    morning_post = True if data['morning_post'] == 'true' else False
    assert url != ''
    assert upper_date_limit != ''
    assert lower_date_limit != ''
    assert len(re.findall(r'-', upper_date_limit)) == 2
    assert len(re.findall(r'-', lower_date_limit)) == 2

    data_of_channel = {
        url: {
            'time_from': upper_date_limit,
            'time_to': lower_date_limit,
            'video_or_photo': video_or_photo,
            'morning_post': morning_post
        }
    }

    client_mongodb.register_entry_channels_config()
    client_mongodb.update_data_in_entity_in_collection_for_parser_configs('from', url, data_of_channel)

    await bot.send_message(chat_id, f'✅︎ Добавил в базу данных канал:\n**{url}**', parse_mode='markdown')

