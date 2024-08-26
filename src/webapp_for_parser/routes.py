from pathlib import Path
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiogram import Bot
from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data
from src.databases.mongodb import client_mongodb
from src.webapp_for_parser.tools_for_regiser_new_channel_in_db import register_channel_from_get_the_posts, register_channel_to_post_the_posts
from src.webapp_for_parser.tools_for_delete_the_channel import Eraser
from src.exceptions.castom_exceptions import Exceptions


async def demo_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / "data_for_webapp/index.html")


async def channel_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / 'data_for_webapp/choose_channel_direction_page.html')


async def direction_from_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / 'data_for_webapp/delete_channel_page_from.html')


async def direction_to_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / 'data_for_webapp/delete_channel_page_to.html')


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

    try:
        if data['direction'] == 'to':
            await register_channel_to_post_the_posts(bot, web_app_init_data.user.id, data)
        elif data['direction'] == 'from':
            await register_channel_from_get_the_posts(bot, web_app_init_data.user.id, data)
    except AssertionError:
        await bot.send_message(web_app_init_data.user.id, '❌︎ Пустые данные были обнаружены в форме.\nЗаполните форму еще раз.')
    return json_response(data={'ok': True}, status=200)


async def delete_channel(request: Request):
    bot: Bot = request.app["bot"]
    data = await request.post()
    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)

    try:
        direction = data['direction']
        channel = data['channel']

        eraser = Eraser(channel, direction)
        eraser.start_erase()

        return json_response({'ok': True}, status=200)

    except Exceptions.ExceptionOnUnFoundChannelInDb:
        await bot.send_message(web_app_init_data.user.id, '❌︎ Не удалось найти выбранный канал в бд.')


async def get_channels(request: Request):
    bot: Bot = request.app["bot"]
    data = await request.post()
    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)

    channels = client_mongodb.get_channels_url(data['direction'])
    return json_response(data={'channels': channels}, status=200)