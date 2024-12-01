from sqlalchemy.orm import Session

from database.core.db import GetSession
from database.models import User


@GetSession
def get_user_token(telegram_id: int, session: Session) -> str | None:
    user = session.get(User, telegram_id)
    if user:
        return user.access_token
    return None
