from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from src.tools_for_tg_bot.Configs.callbacks_configs import CallbacksNames


def actions_markup() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    start_parser_button = InlineKeyboardButton(text='✅ Старт парсер', callback_data=CallbacksNames.start_parser)
    stop_parser_button = InlineKeyboardButton(text='❌ Стоп парсер', callback_data=CallbacksNames.stop_parser)
    check_parser_button = InlineKeyboardButton(text='ℹ️ Проверить парсер', callback_data=CallbacksNames.check_parser)
    add_or_delete_channels_button = InlineKeyboardButton(text='➕ Добавить или ➖ удалить каналы', callback_data=CallbacksNames.add_or_delete_channels)
    change_parameters_in_configs_button = InlineKeyboardButton(text='🔼 Изменить параметры в настройках', callback_data=CallbacksNames.change_parameters)

    keyboard.row(start_parser_button)
    keyboard.row(stop_parser_button)
    keyboard.row(check_parser_button)
    keyboard.row(add_or_delete_channels_button)
    keyboard.row(change_parameters_in_configs_button)

    return keyboard.as_markup()


