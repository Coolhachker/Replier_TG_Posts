import asyncio
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
from src.webapp_for_parser.tools_for_delete_the_channel import Eraser
from src.webapp_for_parser.tools_for_start_channel import start_channel
import logging
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
    async def turn_off_channel_callback(cq: CallbackQuery):
        channel = 'https://t.me/' + cq.data.split('-', maxsplit=1)[1]
        eraser = Eraser(channel, 'to')
        result = eraser.stop_task()
        # await bot.send_message(cq.message.chat.id, result)

    @dispatcher.callback_query(lambda cq: re.search(CallbacksNames.turn_on_channel, cq.data))
    async def turn_on_callback(cq: CallbackQuery):
        channel = 'https://t.me/' + cq.data.split('-', maxsplit=1)[1]
        logger.debug(f'Выбранный канал для включения в системе: {channel}')
        result = start_channel(channel)
        await bot.send_message(cq.message.chat.id, result)



