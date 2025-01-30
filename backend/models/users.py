from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Index, text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .base import BaseModel

if TYPE_CHECKING:
    from .habits import HabitModel


class UserModel(BaseModel):
    """
    Модель пользователя.

    username - юзернейм
    password - пароль
    telegram_id - id пользователя в телеграме
    is_active - True, если пользователь активен, иначе False
    date_of_registration - дата регистрации
    """

    __table_args__ = (
        Index("username_idx", "username"),
        Index("telegram_id_idx", "telegram_id"),
    )
    username: Mapped[str]
    password: Mapped[bytes]
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(default=True)
    date_of_registration: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    habits: Mapped[list["HabitModel"]] = relationship(back_populates="user")
