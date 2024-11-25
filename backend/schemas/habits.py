from pydantic import BaseModel

from schemas.results import ResultSchema


class HabitSchema(BaseModel):
    name: str
    notification_hour: int
    count: int
    description: str = "Пока нет описания"


class HabitCreateSchema(HabitSchema):
    pass


class HabitCompletedSchema(ResultSchema):
    completed: bool


class MarkHabitSchema(BaseModel):
    is_done: bool
    reason: str | None = None
    date: str | None = None
