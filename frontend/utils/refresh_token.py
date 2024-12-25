from collections.abc import Callable
from typing import Any, Required, TypedDict, Unpack

from api.users.get_token import get_new_access_token_by_id
from charset_normalizer.md import getLogger
from database.crud.update_token import update_token_by_id

from .exceptions import InvalidAccessToken

logger = getLogger(__name__)


class ApiOptions(TypedDict, total=False):
    access_token: Required[str]
    is_active: bool
    password: str
    tg_id: int
    name: str
    count: int
    hour: int
    description: str
    number: int
    cache: dict
    habit_id: int
    is_done: str
    date: str
    reason: str | None
    is_complete_null: bool
    new_data: dict


def get_response_and_refresh_token(
    telegram_id: int, func: Callable, **kwargs: Unpack[ApiOptions]
) -> Any:
    """
    Делает запрос на бэкэнд, передавая в функцию func аргументы kwargs.
    Если ответ приходит с ошибкой авторизации, обновляет access_token пользователя в базе
    и делает запрос снова с обновлённым токеном
    :param telegram_id: телеграм id
    :param func: функция для вызова
    :param kwargs: аргументы для func
    :return: результат func
    """
    try:
        return func(**kwargs)
    except InvalidAccessToken:
        logger.info("Просроченный токен у пользователя %s", telegram_id)
        new_access_token = get_new_access_token_by_id(telegram_id)
        update_token_by_id(telegram_id, new_access_token)
        kwargs["access_token"] = new_access_token
        return func(**kwargs)
