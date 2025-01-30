from datetime import date

from models import HabitModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .base import BaseModel


class TrackingModel(BaseModel):
    """
    Модель для отслеживания выполнения привычек пользователя
    date - дата, за которую пользователь отметил привычку, как выполненную или нет
    is_done - True, если задание было выполнено, иначе False
    reason - причина невыполения или None
    habit_id - id привычки
    """

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
