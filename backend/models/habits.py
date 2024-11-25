from datetime import datetime, date

from sqlalchemy import TEXT, ForeignKey, text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import UserModel
    from .tracking import TrackingModel


class HabitModel(BaseModel):
    name: Mapped[str]
    description: Mapped[str] = mapped_column(TEXT)
    notification_hour: Mapped[int]
    count: Mapped[int]
    is_frozen: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    completed_at: Mapped[date | None] = mapped_column(default=None)
    user: Mapped["UserModel"] = relationship(back_populates="habits")
    tracking: Mapped[list["TrackingModel"]] = relationship(back_populates="habit")
