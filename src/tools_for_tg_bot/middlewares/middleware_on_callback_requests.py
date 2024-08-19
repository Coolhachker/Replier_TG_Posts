from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.types import CallbackQuery
from aiogram import Bot


class MiddlewareOnCallback(CallbackAnswerMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event: CallbackQuery, data):
        await self.bot.delete_message(event.message.chat.id, event.message.message_id)
        await handler(event, data)