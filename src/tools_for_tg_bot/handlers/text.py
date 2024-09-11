from aiogram.types import Message
from aiogram import Dispatcher, Bot
import re
from src.tools_for_tg_bot.buttons.actions_markup import actions_markup
from src.tools_for_tg_bot.buttons.button_choose_the_action import choose_the_action_button
from aiogram.fsm.context import FSMContext


def text(dispatcher: Dispatcher, bot: Bot):
    @dispatcher.message(lambda message: re.search('Действия', message.text))
    async def send_the_actions(message: Message):
        await bot.send_message(message.chat.id, 'Выберите действие: ⬇️', reply_markup=actions_markup())

    @dispatcher.message(lambda message: re.search('Вернуться', message.text))
    async def handler_comeback(message: Message, state: FSMContext):
        await state.clear()
        await bot.send_message(message.chat.id, 'Возвращаю вас на главную. 🔙', reply_markup=choose_the_action_button())