from inline.callback.callbacks import CB
from inline.callback.constants import DEFROST_OUTPUT, FREEZE_OUTPUT
from inline.callback.factories import activity_user_factory

from .types import Buttons


def get_freezing_or_defrosting_btn(is_active: bool) -> Buttons:
    """
    Возвращает кнопку для активации или деактивации пользователя
    :param is_active: активен ли пользователь на момент отправки кнопки
    :return: Buttons
    """
    output = FREEZE_OUTPUT if is_active else DEFROST_OUTPUT
    return {output: {CB: activity_user_factory.new(is_active=int(not is_active))}}
