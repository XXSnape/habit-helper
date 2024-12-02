from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup


def create_keyboard(
    *values: dict[str, dict[str, str]], row_width=1
) -> InlineKeyboardMarkup:
    all_values = {}
    for value in values:
        all_values.update(value)

    return quick_markup(all_values, row_width)
