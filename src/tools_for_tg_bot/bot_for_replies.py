from aiogram import Bot, Dispatcher


class BotForReplies:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dispatcher = Dispatcher()
        self.run_sync_functions()

    def run_sync_functions(self):
        pass

    async def start_pooling(self):
        await self.dispatcher.start_polling(self.bot)


if __name__ == '__main__':
    bot = BotForReplies('6356385807:AAHWycJ5m7jykCVRcDCWUa3BvFL_oRlou5k')