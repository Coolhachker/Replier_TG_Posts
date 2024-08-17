from aiogram.types import Message
from aiogram import Dispatcher, Bot
import re
from src.tools_for_tg_bot.buttons.actions_markup import actions_markup


def text(dispatcher: Dispatcher, bot: Bot):
    @dispatcher.message(lambda message: re.search('Действия', message.text))
    async def send_the_actions(message: Message):
        await bot.send_message(message.chat.id, 'Выберите действие: ⬇️', reply_markup=actions_markup())