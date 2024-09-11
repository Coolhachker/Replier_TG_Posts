from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames


def add_or_delete_channels_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    add_button = InlineKeyboardButton(text='➕ Добавить канал', callback_data=CallbacksNames.add_channel)
    delete_button = InlineKeyboardButton(text='➖️ Удалить канал', callback_data=CallbacksNames.delete_channel)

    builder.row(add_button)
    builder.row(delete_button)

    return builder.as_markup()