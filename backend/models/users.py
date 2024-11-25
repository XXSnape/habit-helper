from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column


from .base import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .habits import HabitModel


class UserModel(BaseModel):
    username: Mapped[str]
    password: Mapped[bytes]
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(default=True)
    habits: Mapped[list["HabitModel"]] = relationship(back_populates="user")
