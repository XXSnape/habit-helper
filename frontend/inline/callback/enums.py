from enum import IntEnum, auto


class HabitPropertiesEnum(IntEnum):
    NAME = auto()
    HOUR = auto()
    COUNT = auto()
    DESCRIPTION = auto()
    IS_FROZEN = auto()


class ActionsHabitEnum(IntEnum):
    EDIT = auto()
    DELETE = auto()
    VIEW = auto()
    RESUME = auto()
    FREEZE = auto()
