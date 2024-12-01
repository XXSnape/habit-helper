from telebot.types import InlineKeyboardMarkup

from .general import create_keyboard
from ..buttons.cancel import get_cancel_btn


def get_cancel_kb() -> InlineKeyboardMarkup:
    return create_keyboard(get_cancel_btn())
