from sqlalchemy.orm import Session

from database.core.db import GetSession
from database.models import User


@GetSession
def get_user_token(telegram_id: int, session: Session) -> str | None:
    """
    Получает токен пользователя по его telegram_id из базы
    :param telegram_id: телеграм id
    :param session: сессия для работы с базой
    :return: токен пользователя или None, если он не найден
    """
    user = session.get(User, telegram_id)
    if user:
        return user.access_token
    return None
