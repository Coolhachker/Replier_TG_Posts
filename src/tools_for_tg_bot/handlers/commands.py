from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Dispatcher, Bot


def commands(dispatcher: Dispatcher, bot: Bot):
    @dispatcher.message(CommandStart())
    async def handle_start_command(message: Message):
        await bot.send_message(message.chat.id, 'Здравствуйте, это 🤖 бот для работы с парсером постов в телеграме.')