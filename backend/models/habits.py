from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from .base import BaseModel


class HabitModel(BaseModel):
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(TEXT, default=None)
    notification_hour: Mapped[int | None] = mapped_column(default=None)
    count: Mapped[int | None] = mapped_column(default=None)
    is_done: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = ForeignKey("users.id", ondelete="CASCADE")
