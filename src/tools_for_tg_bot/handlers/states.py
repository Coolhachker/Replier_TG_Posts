import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.tools_for_tg_bot.Configs.States import States
from src.webapp_for_parser.tools_for_delete_the_channel import Eraser
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames
import datetime
from src.tools_for_tg_bot.buttons.button_choose_the_action import choose_the_action_button
from src.webapp_for_parser.tools_for_start_channel import start_channel
import logging
from src.databases.mysqldb import client_mysqldb
logger = logging.getLogger()


def state_handlers(bot: Bot, dispatcher: Dispatcher):
    @dispatcher.message(States.get_date)
    async def handler_date_for_turn_off_channel(message: Message, state: FSMContext):
        try:
            data = await state.get_data()
            datetime_now = datetime.datetime.now()
            time_zone = datetime.timezone(datetime.timedelta(hours=3), name='МСК')
            datetime_now = datetime_now.timestamp() + time_zone.utcoffset(datetime_now).total_seconds()

            delay = datetime.datetime.strptime(message.text, "%d-%m-%Y %H:%M").timestamp() - datetime_now if message.text != 'Сейчас' else 0
            assert delay >= 0

            await state.clear()
            await bot.send_message(message.chat.id, 'Возвращаю вас на главную. 🔙', reply_markup=choose_the_action_button())

            await asyncio.sleep(delay)

            if data['command'] == CallbacksNames.turn_off_channel:
                eraser = Eraser(data["channel"], 'to')
                eraser.stop_task()
                # await bot.send_message(cq.message.chat.id, result)
            elif data['command'] == CallbacksNames.turn_on_channel:
                result = start_channel(data['channel'])
                await bot.send_message(message.chat.id, result)
        except (AttributeError, Exception):
            await bot.send_message(message.chat.id, '❌︎ Произошла ошибка несоответствия форматов.\n🔄 Введите дату еще раз')

    @dispatcher.message(States.set_admin)
    async def handler_on_set_admin(message: Message, state: FSMContext):
        client_mysqldb.add_entry_in_trusted_users(message.text)
        await state.clear()
        await bot.send_message(message.chat.id, '✅︎ Администратор был успешно добавлен', reply_markup=choose_the_action_button())