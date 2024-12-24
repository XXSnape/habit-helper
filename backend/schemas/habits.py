from typing import Annotated

from pydantic import BaseModel, Field
from datetime import date as datetime_date, datetime
from schemas.results import ResultSchema


class HabitSchema(BaseModel):
    """
    Схема для частичного представления привычки

    name - название
    notification_hour - час напоминания
    count - количество дней для формирования привычки
    description - описание
    """

    name: str
    notification_hour: Annotated[int, Field(le=23, ge=0)]
    count: Annotated[int, Field(ge=1)]
    description: str = "Пока нет описания"


class HabitNameSchema(BaseModel):
    """
    Схема для представления названия привычки

    name - название
    """

    name: str


class TrackingSchema(BaseModel):
    """
    Схема для представления информации о дате и статусе выполнения действия

    is_done - True, если пользователь выполнил действие для формирования привычки, иначе False
    date - дата для пометки
    reason - причина невыполнения или None
    """

    is_done: bool
    date: datetime_date
    reason: str | None


class HabitOutputSchema(HabitSchema):
    """
    Полное представление о привычке

    id - id в базе
    is_frozen - приостановлена привычка или нет
    created_at - дата и время создания
    tracking - дополнительная статистическая информация
    """

    id: int
    is_frozen: bool
    created_at: datetime | None
    tracking: list[TrackingSchema]


class HabitPatchSchema(BaseModel):
    """
    Схема для обновления информации о привычке.
    Все параметры опциональны.

    name - название
    description - описание
    notification_hour - час для отправки напоминания
    count - количество дней для формирования привычки
    is_frozen - True, если привычка должна быть приостановлена, иначе False.
    """

    name: str | None = None
    description: str | None = None
    notification_hour: Annotated[int | None, Field(le=23, ge=0)] = None
    count: Annotated[int | None, Field(ge=1)] = None
    is_frozen: bool | None = None


class HabitCreateSchema(HabitSchema):
    """
    Схема для создания привычки
    """

    pass


class HabitCompletedSchema(ResultSchema):
    """
    Схема для представления, сформирована ли привычка или нет
    completed - True, если привычка сформирована, иначе False
    """

    completed: bool


class HabitResumeSchema(BaseModel):
    """
    Схема для возобновления сформированной привычки

    count - новое число дней для формирования привычки
    """

    count: Annotated[int | None, Field(ge=1)]


class MarkHabitSchema(BaseModel):
    """
    Схема для представления информации о выполнении действий для формирования привычки

    is_done - выполнены действия или нет
    date - дата выполнения действий
    reason - причина невыполнения
    """

    is_done: bool
    date: str
    reason: str | None = None
