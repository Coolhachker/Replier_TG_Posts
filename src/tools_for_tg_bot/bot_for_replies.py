import asyncio
from src.tools_for_tg_bot.handlers.commands import commands
from src.tools_for_tg_bot.handlers.text import text
from src.tools_for_tg_bot.handlers.callbacks import callbacks
from src.tools_for_tg_bot.handlers.states import state_handlers
from aiogram import Bot, Dispatcher
from src.tools_for_tg_bot.middlewares.middleware_on_check_trusted_users import MiddlewareOnTrustUser
from src.tools_for_tg_bot.middlewares.middleware_on_callback_requests import MiddlewareOnCallback
from src.tools_for_tg_bot.handlers.rabbitmq_handler import handler_info_responses, ping_the_parser
from aiogram import Router


class BotForReplies:
    def __init__(self, token):
        self.router = Router()
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        self.dispatcher.include_router(self.router)
        self.run_sync_functions()

    def run_sync_functions(self):
        commands(self.dispatcher, self.bot)
        text(self.dispatcher, self.bot)
        callbacks(self.dispatcher, self.bot)
        state_handlers(self.bot, self.dispatcher)

    async def start_pooling(self):
        asyncio.create_task(ping_the_parser(self.bot))
        asyncio.create_task(handler_info_responses(self.bot))
        self.dispatcher.message.middleware(MiddlewareOnTrustUser(self.bot))
        self.dispatcher.callback_query.middleware(MiddlewareOnCallback(self.bot))
        # await self.dispatcher.start_polling(self.bot)


# if __name__ == '__main__':
    # bot = BotForReplies('6356385807:AAHWycJ5m7jykCVRcDCWUa3BvFL_oRlou5k')
    # asyncio.run(bot.start_pooling())