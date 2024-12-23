from .types import Buttons

from inline.callback.callbacks import CB
from inline.callback.constants import FREEZE_OUTPUT, DEFROST_OUTPUT
from inline.callback.factories import activity_user_factory


def get_freezing_or_defrosting_btn(is_active: bool) -> Buttons:
    """
    Возвращает кнопку для активации или деактивации пользователя
    :param is_active: активен ли пользователь на момент отправки кнопки
    :return: Buttons
    """
    output = FREEZE_OUTPUT if is_active else DEFROST_OUTPUT
    return {output: {CB: activity_user_factory.new(is_active=int(not is_active))}}
