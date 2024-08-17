from aiogram import BaseMiddleware, Bot
from src.databases.mysqldb import client_mysqldb


class MiddlewareOnTrustUser(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(self, handler, event, data):
        client_mysqldb.cursor.execute('SELECT user_nickname FROM trusted_users')
        trusted_users = [user[0] for user in client_mysqldb.cursor.fetchall()]
        if event.from_user.username in trusted_users:
            await handler(event, data)
        else:
            await self.bot.send_message(event.chat.id, '❌️ У вас нет прав на использование этого бота.')