from aiogram import BaseMiddleware, Bot


class MiddlewareOnTrustUser(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    def __call__(self, handler, event, data):
        pass