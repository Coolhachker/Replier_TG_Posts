from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import WebAppInfo
from src.tools_for_tg_bot.Configs.Config_base_url import BaseURL


def button_on_change_param() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    button = InlineKeyboardButton(text='Нажмите', web_app=WebAppInfo(url=BaseURL.URL + '/channel/change_the_settings_in_channel'))

    builder.row(button)

    return builder.as_markup()