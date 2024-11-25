from sqlalchemy import Date, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from datetime import date

from models import HabitModel
from .base import BaseModel


class TrackingModel(BaseModel):
    __tablename__ = "tracking"

    __table_args__ = (
        UniqueConstraint(
            "date",
            "habit_id",
            name="idx_uniq_date_habit",
        ),
    )

    date: Mapped[date]
    is_done: Mapped[bool] = mapped_column(default=True)
    reason: Mapped[str | None] = mapped_column(default=None)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))
    habit: Mapped["HabitModel"] = relationship(back_populates="tracking")
