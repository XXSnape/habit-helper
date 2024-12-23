from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from inline.buttons.types import Buttons


def create_keyboard(*values: Buttons, row_width=1) -> InlineKeyboardMarkup:
    """
    Универсальная функция для генерации клавиатуры

    :param values: объекты Buttons
    :param row_width: отвечает за то, сколько кнопок могу находиться в одной строке
    :return: InlineKeyboardMarkup
    """
    all_values = {}
    for value in values:
        all_values.update(value)

    return quick_markup(all_values, row_width)
