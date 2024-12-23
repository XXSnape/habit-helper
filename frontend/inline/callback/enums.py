from enum import IntEnum, auto


class HabitPropertiesEnum(IntEnum):
    """
    Параметры привычки

    NAME - название
    HOUR - час, в который нужно отправлять уведомление
    COUNT - количество дней для привития
    DESCRIPTION - описание
    IS_FROZEN - статус активности
    """

    NAME = auto()
    HOUR = auto()
    COUNT = auto()
    DESCRIPTION = auto()
    IS_FROZEN = auto()


class ActionsHabitEnum(IntEnum):
    """
    Действия с привычкой

    EDIT - редактировать
    DELETE - удалить
    VIEW - просмотреть
    RESUME - возобновить
    FREEZE - приостановить
    """

    EDIT = auto()
    DELETE = auto()
    VIEW = auto()
    RESUME = auto()
    FREEZE = auto()
