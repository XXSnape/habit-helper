from telebot.types import InlineKeyboardButton

from keyboards.inline.callback.callbacks import CALL_OFF_CALLBACK
from keyboards.inline.callback.constants import CALL_OFF_OUTPUT


def get_cancel_btn():
    return InlineKeyboardButton(text=CALL_OFF_OUTPUT, callback_data=CALL_OFF_CALLBACK)
