from inline.buttons.cancel import get_home_btn
from inline.callback.callbacks import CB, LOG_IN_CALLBACK, REGISTRATION_CALLBACK
from inline.callback.constants import LOG_IN_OUTPUT, MENU_OUTPUT, REGISTER_OUTPUT

from .types import Buttons


def get_check_in_buttons() -> Buttons:
    """
    Возвращает кнопки для регистрации или входа в аккаунт
    :return: Buttons
    """
    return {
        REGISTER_OUTPUT: {CB: REGISTRATION_CALLBACK},
        LOG_IN_OUTPUT: {CB: LOG_IN_CALLBACK},
        **get_home_btn(MENU_OUTPUT),
    }
