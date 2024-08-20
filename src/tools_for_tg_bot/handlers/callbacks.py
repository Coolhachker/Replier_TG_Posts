from aiogram import Dispatcher, Bot
from aiogram.types import CallbackQuery
from src.rabbitmq_tools.producer import producer
from src.rabbitmq_tools.producer_commands import Commands


def callbacks(dispatcher: Dispatcher, bot: Bot):
    @dispatcher.callback_query(lambda cq: cq.data == 'start_parser')
    async def callback_on_start_parser(cq: CallbackQuery):
        result = producer.publish(Commands.TURN_ON_COMMAND)
        await bot.send_message(cq.message.chat.id, result)

    @dispatcher.callback_query(lambda cq: cq.data == 'stop_parser')
    async def callback_on_stop_parser(cq: CallbackQuery):
        result = producer.publish(Commands.TURN_OFF_COMMAND)
        await bot.send_message(cq.message.chat.id, result)

    @dispatcher.callback_query(lambda cq: cq.data == 'check_parser')
    async def callback_on_check_parser(cq: CallbackQuery):
        result = producer.publish(Commands.CHECK_PARSER_COMMAND)
        await bot.send_message(cq.message.chat.id, result)
