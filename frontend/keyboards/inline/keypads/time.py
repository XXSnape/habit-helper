from telebot.types import InlineKeyboardMarkup

from keyboards.inline.buttons.cancel import get_cancel_dict
from keyboards.inline.buttons.time import get_hours_buttons
from keyboards.inline.keypads.general import create_keyboard


def get_hour_selection_kb() -> InlineKeyboardMarkup:
    values = get_hours_buttons()
    values.update(get_cancel_dict())
    return create_keyboard(values=values, row_width=4)
