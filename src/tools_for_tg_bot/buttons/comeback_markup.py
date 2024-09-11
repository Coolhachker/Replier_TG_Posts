from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton


def set_comeback_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    button_comeback = KeyboardButton(text='↩️ Вернуться')

    builder.row(button_comeback)

    return builder.as_markup(resize_keyboard=True)
