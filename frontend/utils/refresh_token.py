from collections.abc import Callable

from charset_normalizer.md import getLogger

from api.users.get_token import get_new_access_token_by_id
from database.crud.update_token import update_token_by_id
from .exceptions import InvalidAccessToken

logger = getLogger(__name__)


def get_response_and_refresh_token(telegram_id: int, func: Callable, **kwargs):
    try:
        return func(**kwargs)
    except InvalidAccessToken:
        logger.info("Просроченный токен")
        new_access_token = get_new_access_token_by_id(telegram_id)
        update_token_by_id(telegram_id, new_access_token)
        kwargs["access_token"] = new_access_token
        return func(**kwargs)


# class RefreshToken:
#     def __init__(self, func: Callable):
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         try:
#             return self.func(*args, **kwargs)
#         except InvalidAccessToken:
#             logger.info('Просроченный токен')
