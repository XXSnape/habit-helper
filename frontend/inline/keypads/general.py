from inline.buttons.types import Buttons
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import quick_markup


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
