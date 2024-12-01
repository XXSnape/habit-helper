from telebot.types import InlineKeyboardButton

from keyboards.inline.callback.callbacks import REGISTRATION_CALLBACK, DELETE_CALLBACK
from keyboards.inline.callback.constants import REGISTER_OUTPUT, DELETE_MSG_OUTPUT


def get_check_in_btn():
    return InlineKeyboardButton(
        text=REGISTER_OUTPUT, callback_data=REGISTRATION_CALLBACK
    )


def get_delete_psw_ptn():
    return InlineKeyboardButton(text=DELETE_MSG_OUTPUT, callback_data=DELETE_CALLBACK)
