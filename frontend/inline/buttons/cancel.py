from inline.callback.callbacks import (CALL_OFF_CALLBACK, CB,
                                       REFUSAL_TO_DESCRIBE_CALLBACK)
from inline.callback.constants import (CALL_OFF_OUTPUT,
                                       REFUSAL_TO_DESCRIBE_OUTPUT)

from .types import Buttons


def get_home_btn(output=CALL_OFF_OUTPUT) -> Buttons:
    """
    Возвращает кнопку для получения информации о командах
    :param output: надпись на кнопке
    :return: Buttons
    """
    return {output: {CB: CALL_OFF_CALLBACK}}


def get_refusal_to_describe_btn() -> Buttons:
    """
    Возвращает кнопку, чтобы не задавать описание привычке
    :return: Buttons
    """
    return {REFUSAL_TO_DESCRIBE_OUTPUT: {CB: REFUSAL_TO_DESCRIBE_CALLBACK}}
