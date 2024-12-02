from telebot.types import InlineKeyboardButton

from keyboards.inline.callback.callbacks import (
    REGISTRATION_CALLBACK,
    DELETE_CALLBACK,
    CB,
)
from keyboards.inline.callback.constants import REGISTER_OUTPUT, DELETE_MSG_OUTPUT


def get_check_in_btn():
    return {REGISTER_OUTPUT: {CB: REGISTRATION_CALLBACK}}


def get_delete_psw_ptn():
    return {DELETE_MSG_OUTPUT: {CB: DELETE_CALLBACK}}
