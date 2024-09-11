import re
from aiogram import Dispatcher, Bot
from aiogram.types import CallbackQuery
from src.rabbitmq_tools.producer import producer
from src.rabbitmq_tools.producer_commands import Commands
from src.tools_for_tg_bot.buttons.add_or_delete_channels_merkup import add_or_delete_channels_markup
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames
from src.tools_for_tg_bot.buttons.webapp_on_add_channel import button_on_add_channel
from src.tools_for_tg_bot.buttons.webapp_on_delete_channel import button_on_delete_channel
from src.tools_for_tg_bot.buttons.webapp_on_change_parameters import button_on_change_param
from src.tools_for_tg_bot.buttons.channels_markup import set_channels_markup
import logging
from aiogram.fsm.context import FSMContext
from src.tools_for_tg_bot.Configs.States import States
from src.tools_for_tg_bot.buttons.markup_for_get_date import set_markup_for_get_date
from src.tools_for_tg_bot.buttons.admins_markup import set_admins_markup
from src.databases.mysqldb import client_mysqldb
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from src.tools_for_tg_bot.buttons.comeback_markup import set_comeback_markup
logger = logging.getLogger()


def callbacks(dispatcher: Dispatcher, bot: Bot):
    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.start_parser)
    async def callback_on_start_parser(cq: CallbackQuery):
        result = producer.publish(Commands.TURN_ON_COMMAND)
        await bot.send_message(cq.message.chat.id, result)

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.stop_parser)
    async def callback_on_stop_parser(cq: CallbackQuery):
        result = producer.publish(Commands.TURN_OFF_COMMAND)
        await bot.send_message(cq.message.chat.id, result)

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.check_parser)
    async def callback_on_check_parser(cq: CallbackQuery):
        result = producer.publish(Commands.CHECK_PARSER_COMMAND)
        await bot.send_message(cq.message.chat.id, result)

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.add_or_delete_channels)
    async def callback_on_add_or_delete_channels(cq: CallbackQuery):
        await bot.send_message(cq.message.chat.id, 'Выберите действие: ⬇️', reply_markup=add_or_delete_channels_markup())

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.add_channel)
    async def callback_on_add_channel(cq: CallbackQuery):
        await bot.send_message(cq.message.chat.id, 'Нажмите на кнопку для продолжения действия.', reply_markup=button_on_add_channel())

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.delete_channel)
    async def callback_on_delete_channel(cq: CallbackQuery):
        await bot.send_message(cq.message.chat.id, 'Нажмите на кнопку для продолжения действия.', reply_markup=button_on_delete_channel())

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.change_parameters)
    async def callback_on_change_parameters(cq: CallbackQuery):
        await bot.send_message(cq.message.chat.id, 'Нажмите на кнопку для продолжения действия.', reply_markup=button_on_change_param())

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.get_channels)
    async def callback_on_get_channels(cq: CallbackQuery):
        result = producer.publish(Commands.GET_CHANNELS_COMMAND)
        logger.debug(f'Список чатов: {result}')
        await bot.send_message(cq.message.chat.id, 'ℹ️ Этот раздел посвящен остановке или включению каналов в системе.\nЕсли вам нужно остановить канал, у которого стоит напротив галочка - ✅︎, то нажмите на него.\nОбратно если хотите включить канал.', reply_markup=set_channels_markup(result))

    @dispatcher.callback_query(lambda cq: re.search(CallbacksNames.turn_off_channel, cq.data))
    async def turn_off_channel_callback(cq: CallbackQuery, state: FSMContext):
        channel = 'https://t.me/' + cq.data.split('-', maxsplit=1)[1]
        await state.set_data({'channel': channel, 'command': CallbacksNames.turn_off_channel})
        await state.set_state(States.get_date)
        await bot.send_message(cq.message.chat.id, '🗓 Напишите время остановки парсера в формате\n\tDAY-MONTH-YEAR HOUR:MINUTE', reply_markup=set_markup_for_get_date())

    @dispatcher.callback_query(lambda cq: re.search(CallbacksNames.turn_on_channel, cq.data))
    async def turn_on_callback(cq: CallbackQuery, state: FSMContext):
        channel = 'https://t.me/' + cq.data.split('-', maxsplit=1)[1]
        logger.debug(f'Выбранный канал для включения в системе: {channel}')
        channel = 'https://t.me/' + cq.data.split('-', maxsplit=1)[1]
        await state.set_data({'channel': channel, 'command': CallbacksNames.turn_on_channel})
        await state.set_state(States.get_date)
        await bot.send_message(cq.message.chat.id, '🗓 Напишите время включения парсера в формате\n\tDAY-MONTH-YEAR HOUR:MINUTE', reply_markup=set_markup_for_get_date())

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.admins)
    async def callback_on_admins(cq: CallbackQuery):
        await bot.send_message(cq.message.chat.id, 'Выберите действие ⬇️', reply_markup=set_admins_markup())

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.list_of_admins)
    async def callback_on_list_of_admins(cq: CallbackQuery, page=1):
        admins = client_mysqldb.get_nicknames_of_trusted_user()

        left = page - 1 if page != 1 else admins
        right = page + 1 if page != admins else 1

        builder = InlineKeyboardBuilder()

        button_left = InlineKeyboardButton(text='<-', callback_data=f'left_admin {left}')
        button_right = InlineKeyboardButton(text='->', callback_data=f'right_admin {right}')
        submit_button = InlineKeyboardButton(text='Удалить', callback_data=CallbacksNames.delete_admin)

        builder.row(button_left, button_right)
        builder.row(submit_button)
        try:
            await bot.send_message(cq.message.chat.id, admins[page - 1], reply_markup=builder.as_markup())
        except:
            pass

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.add_admin)
    async def callback_on_add_admin(cq: CallbackQuery, state: FSMContext):
        await state.set_state(States.set_admin)
        await bot.send_message(cq.message.chat.id, '✍🏼 Введите username администратора, которого хотите добавить.', reply_markup=set_comeback_markup())

    @dispatcher.callback_query(lambda cq: re.search('left_admin', cq.data))
    async def callback_on_left_button(cq: CallbackQuery):
        page = int(cq.data.split(' ')[1])
        await callback_on_list_of_admins(cq, page=page)

    @dispatcher.callback_query(lambda cq: re.search('right_admin', cq.data))
    async def callback_on_right_button(cq: CallbackQuery):
        page = int(cq.data.split(' ')[1])
        await callback_on_list_of_admins(cq, page=page)

    @dispatcher.callback_query(lambda cq: cq.data == CallbacksNames.delete_admin)
    async def callback_on_delete_admin(cq: CallbackQuery):
        try:
            client_mysqldb.delete_admin_from_db(cq.message.text)
            await bot.send_message(cq.message.chat.id, '✅️ Успешное удаление администратора')
        except:
            await bot.send_message(cq.message.chat.id, '❌︎ Администратор не удалился')





