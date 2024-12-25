from database.core.db import GetSession
from database.models import User
from sqlalchemy.orm import Session


@GetSession
def update_token_by_id(telegram_id: int, access_token: str, session: Session) -> None:
    """
    Обновляет токен по telegram_id
    :param telegram_id: телеграм id
    :param access_token: новый токен пользователя
    :param session: сессия для работы с базой
    """
    user = session.get(User, telegram_id)
    user.access_token = access_token
    session.commit()


@GetSession
def update_telegram_id_and_token(
    old_telegram_id: int, new_telegram_id: int, access_token: str, session: Session
) -> None:
    """
    Обновляет телеграм id пользователю и токен
    :param old_telegram_id: старый телеграм id
    :param new_telegram_id: новый телеграм id
    :param access_token: токен пользователя
    :param session: сессия для работы с базой
    """
    user = session.get(User, old_telegram_id)
    user.telegram_id = new_telegram_id
    user.access_token = access_token
    session.commit()
