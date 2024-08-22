from pathlib import Path
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiogram import Bot
from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from src.databases.mongodb import client_mongodb
import re


async def demo_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / "data_for_webapp/index.html")


async def check_data_handler(request: Request):
    bot: Bot = request.app["bot"]

    data = await request.post()
    if check_webapp_signature(bot.token, data["_auth"]):
        return json_response({"ok": True})
    return json_response({"ok": False, "err": "Unauthorized"}, status=401)


async def send_form_handler(request: Request):
    bot: Bot = request.app["bot"]
    data = await request.post()
    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)

    print(data)
    try:
        if data['direction'] == 'to':
            await register_channel_to_post_the_posts(bot, web_app_init_data.user.id, data)
        elif data['direction'] == 'from':
            await register_channel_from_get_the_posts(bot, web_app_init_data.user.id, data)
    except AssertionError:
        await bot.send_message(web_app_init_data.user.id, '❌︎ Пустые данные были обнаружены в форме.\nЗаполните форму еще раз.')
    return json_response(data={'ok': True}, status=200)


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

