from aiogram import Dispatcher, Bot
from aiogram.types import CallbackQuery
from src.rabbitmq_tools.producer import producer
from src.rabbitmq_tools.producer_commands import Commands
from src.tools_for_tg_bot.buttons.add_or_delete_channels_merkup import add_or_delete_channels_markup
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames
from src.tools_for_tg_bot.buttons.webapp_on_add_channel import button_on_add_channel
from src.tools_for_tg_bot.buttons.webapp_on_delete_channel import button_on_delete_channel
from src.tools_for_tg_bot.buttons.webapp_on_change_parameters import button_on_change_param


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
        pass
