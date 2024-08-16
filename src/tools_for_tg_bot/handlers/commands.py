from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Dispatcher, Bot
from src.tools_for_tg_bot.buttons.button_choose_the_action import choose_the_action_button


def commands(dispatcher: Dispatcher, bot: Bot):
    @dispatcher.message(CommandStart())
    async def handle_start_command(message: Message):
        await bot.send_message(message.chat.id, 'Здравствуйте, это 🤖 бот для работы с парсером постов в телеграме.', reply_markup=choose_the_action_button())

