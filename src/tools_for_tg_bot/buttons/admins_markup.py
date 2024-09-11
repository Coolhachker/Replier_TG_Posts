from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames


def set_admins_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    delete_admin_button = InlineKeyboardButton(text='👤 Список администраторов', callback_data=CallbacksNames.list_of_admins)
    add_administrator = InlineKeyboardButton(text='➕ Добавить администратора', callback_data=CallbacksNames.add_admin)

    builder.row(delete_admin_button)
    builder.row(add_administrator)

    return builder.as_markup()
