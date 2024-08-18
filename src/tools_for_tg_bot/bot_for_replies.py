import asyncio
from src.tools_for_tg_bot.handlers.commands import commands
from src.tools_for_tg_bot.handlers.text import text
from src.tools_for_tg_bot.handlers.callbacks import callbacks
from aiogram import Bot, Dispatcher
from src.tools_for_tg_bot.middlewares.middleware_on_check_trusted_users import MiddlewareOnTrustUser
from src.tools_for_tg_bot.handlers.rabbitmq_handler import handler_info_responses


class BotForReplies:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        self.run_sync_functions()

    def run_sync_functions(self):
        commands(self.dispatcher, self.bot)
        text(self.dispatcher, self.bot)
        callbacks(self.dispatcher, self.bot)

    async def start_pooling(self):
        asyncio.create_task(handler_info_responses(self.bot))
        self.dispatcher.message.middleware(MiddlewareOnTrustUser(self.bot))
        await self.dispatcher.start_polling(self.bot)


if __name__ == '__main__':
    bot = BotForReplies('6356385807:AAHWycJ5m7jykCVRcDCWUa3BvFL_oRlou5k')
    asyncio.run(bot.start_pooling())