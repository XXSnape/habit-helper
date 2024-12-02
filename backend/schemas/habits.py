from typing import Annotated

from pydantic import BaseModel, Field
from datetime import date as datetime_date, datetime
from schemas.results import ResultSchema


class HabitSchema(BaseModel):
    name: str
    notification_hour: Annotated[int, Field(le=23, ge=0)]
    count: Annotated[int, Field(ge=1)]
    description: str = "Пока нет описания"


class TrackingSchema(BaseModel):
    is_done: bool
    date: datetime_date
    reason: str | None


class HabitOutputSchema(HabitSchema):
    id: int
    is_frozen: bool
    created_at: datetime | None
    tracking: list[TrackingSchema]


class HabitPatchSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    notification_hour: Annotated[int | None, Field(le=23, ge=0)] = None
    count: Annotated[int | None, Field(ge=1)] = None
    is_frozen: bool | None = None


class HabitCreateSchema(HabitSchema):
    pass


class ReasonChangeSchema(BaseModel):
    reason: str


class HabitCompletedSchema(ResultSchema):
    completed: bool


class HabitResumeSchema(BaseModel):
    count: Annotated[int | None, Field(ge=1)]


class MarkHabitSchema(BaseModel):
    is_done: bool
    date: str
    reason: str | None = None
