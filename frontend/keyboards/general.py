from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard(texts_and_callbacks: list[list[str, str]]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for data in texts_and_callbacks:
        markup.add(InlineKeyboardButton(text=data[0], callback_data=data[1]))
    return markup
