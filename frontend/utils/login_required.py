from database.crud.check_user import get_user_token
from telebot import State, TeleBot
from utils.cache_keys import TOKEN_KEY
from utils.exceptions import TokenMissing


def check_registration(
    telegram_id: int, bot: TeleBot, state: State | None = None
) -> str:
    """
    Проверяет, что пользователь с id telegram_id есть в базе.
    Если нет, вызывает исключение TokenMissing.
    Устанавливает новое состояние, если оно передано
    :param telegram_id: телеграм id
    :param bot: TeleBot
    :param state: State | None
    :return: токен пользователя
    """
    token = get_user_token(telegram_id)
    if not token:
        raise TokenMissing
    if state:
        bot.set_state(user_id=telegram_id, chat_id=telegram_id, state=state)
        with bot.retrieve_data(telegram_id, telegram_id) as data:
            data[TOKEN_KEY] = token
    return token
