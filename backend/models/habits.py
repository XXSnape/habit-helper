from datetime import datetime

from sqlalchemy import TEXT, ForeignKey, text
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from .base import BaseModel


class HabitModel(BaseModel):
    name: Mapped[str]
    description: Mapped[str] = mapped_column(TEXT, default="Пока нет описания")
    notification_hour: Mapped[int]
    count: Mapped[int]
    is_done: Mapped[bool] = mapped_column(default=False)
    is_frozen: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
