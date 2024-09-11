from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames


def turn_on_or_turn_off_button(turn_on_or_turn_off: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if turn_on_or_turn_off:
        builder.row(InlineKeyboardButton(text='✅️ Включить', callback_data=CallbacksNames.turn_on_channel))
    else:
        builder.row(InlineKeyboardButton(text='❌️ Выключить', callback_data=CallbacksNames.turn_off_channel))