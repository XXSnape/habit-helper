from sqlalchemy import Date, func, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from datetime import date

from .base import BaseModel


class TrackingModel(BaseModel):
    __tablename__ = "tracking"

    date: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    is_done: Mapped[bool] = mapped_column(default=True)
    reason: Mapped[str | None] = mapped_column(default=None)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
