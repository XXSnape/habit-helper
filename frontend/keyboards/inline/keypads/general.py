from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup


def create_keyboard(
    *buttons: InlineKeyboardButton,
    values: dict[str, dict[str, str]] | None = None,
    row_width=1
) -> InlineKeyboardMarkup:
    if buttons:
        markup = InlineKeyboardMarkup(row_width=row_width)
        for btn in buttons:
            markup.add(btn)
        return markup
    return quick_markup(values, row_width)
