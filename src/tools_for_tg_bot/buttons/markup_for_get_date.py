from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton


def set_markup_for_get_date() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    button_now = KeyboardButton(text='Сейчас')
    button_comeback = KeyboardButton(text='↩️ Вернуться')

    builder.row(button_now)
    builder.row(button_comeback)

    return builder.as_markup(resize_keyboard=True)