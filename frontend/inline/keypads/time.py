from telebot.types import InlineKeyboardMarkup

from inline.buttons.cancel import get_home_btn
from inline.buttons.habits import get_selection_to_edit_btn
from inline.buttons.time import get_hours_buttons
from inline.callback.constants import BACK_OUTPUT
from inline.keypads.general import create_keyboard


def get_hour_selection_kb() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для выбора времени
    :return: InlineKeyboardMarkup
    """

    return create_keyboard(get_hours_buttons(), get_home_btn(), row_width=4)


def get_hour_selection_and_back_kb(number: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для обновления времени отправки привычки
    :param number: номер привычки в кэше
    :return: InlineKeyboardMarkup
    """
    return create_keyboard(
        get_hours_buttons(),
        get_selection_to_edit_btn(number, key=BACK_OUTPUT),
        row_width=4,
    )
