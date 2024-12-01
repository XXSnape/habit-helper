from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard(*buttons: InlineKeyboardButton) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for btn in buttons:
        markup.add(btn)
    return markup
