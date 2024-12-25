from utils.output import get_format_hour

from .types import Buttons


def get_hours_buttons() -> Buttons:
    """
    Возвращает кнопки для выбора времени
    :return: Buttons
    """

    return {get_format_hour(hour): {"callback_data": str(hour)} for hour in range(24)}
