from enum import StrEnum, IntEnum, auto


class HabitProperties(StrEnum):
    NAME = "name"
    HOUR = "hour"
    COUNT = "count"
    DESCRIPTION = "description"
    IS_FROZEN = "is_frozen"


class ActionsHabitEnum(IntEnum):
    EDIT = auto()
    DELETE = auto()
