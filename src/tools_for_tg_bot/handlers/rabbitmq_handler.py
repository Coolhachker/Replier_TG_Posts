import asyncio
from src.databases.mysqldb import client_mysqldb
from aiogram import Bot
from src.rabbitmq_tools.producer import producer


async def handler_info_responses(bot: Bot):
    while True:
        if producer.info_response is None:
            await asyncio.sleep(5)
        else:
            trusted_user = client_mysqldb.get_chat_id_of_trusted_users()
            for user in trusted_user:
                await bot.send_message(user, producer.info_response)
            producer.info_response = None


async def ping_the_parser(bot: Bot):
    while True:
        result = producer.publish('ping', queue=producer.ping_queue)
        if result is None:
            trusted_user = client_mysqldb.get_chat_id_of_trusted_users()
            for user in trusted_user:
                await bot.send_message(user, '⛔️ Произошла ошибка в работе сервиса!\nОбратитесь к инженеру для просмотра журнала.')
                break
        else:
            await asyncio.sleep(30)
            continue
