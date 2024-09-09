import re
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton


def set_channels_markup(string_of_channels: str) -> InlineKeyboardMarkup:
    list_of_channels_to_post_the_posts: list[str] = string_of_channels.split('\n')
    builder = InlineKeyboardBuilder()

    for channel in list_of_channels_to_post_the_posts:
        if re.search('✅', channel):
            button = InlineKeyboardButton(text=channel, callback_data=CallbacksNames.turn_off_channel + '-' + channel.split(' ')[0].split('/')[-1])
            builder.row(button)
        elif re.search('❌️', channel):
            button = InlineKeyboardButton(text=channel, callback_data=CallbacksNames.turn_on_channel + '-' + channel.split(' ')[0].split('/')[-1])
            builder.row(button)

    return builder.as_markup()
