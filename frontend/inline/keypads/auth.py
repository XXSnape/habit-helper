from telebot.types import InlineKeyboardMarkup

from inline.buttons.auth import get_check_in_buttons
from inline.buttons.cancel import get_home_btn
from inline.keypads.general import create_keyboard


def get_auth_request_kb() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для регистрации или входа в аккаунт
    :return: InlineKeyboardMarkup
    """

    return create_keyboard(get_check_in_buttons())
