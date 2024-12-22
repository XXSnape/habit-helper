from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    """
    Модель пользователя

    telegram_id - телеграм id
    access_token - токен для доступа к данным пользователя из бэкэнда
    """

    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str]
