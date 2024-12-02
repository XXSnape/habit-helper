from enum import StrEnum, IntEnum, auto


class HabitProperties(IntEnum):
    NAME = auto()
    HOUR = auto()
    COUNT = auto()
    DESCRIPTION = auto()
    IS_FROZEN = auto()


class ActionsHabitEnum(IntEnum):
    EDIT = auto()
    DELETE = auto()
