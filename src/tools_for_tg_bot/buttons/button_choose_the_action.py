from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, KeyboardButton


def choose_the_action_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    button = KeyboardButton(text='⬇️ Действия')
    keyboard.add(button)

    return keyboard.as_markup(resize_keyboard=True)