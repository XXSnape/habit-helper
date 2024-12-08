from telebot import TeleBot, State

from database.crud.check_user import get_user_token
from keyboards.inline.keypads.auth import get_auth_request_kb
from utils.constants import TOKEN_KEY


def check_registration(
    telegram_id: int, bot: TeleBot, state: State | None = None
) -> str | None:
    token = get_user_token(telegram_id)
    if not token:
        bot.send_message(
            telegram_id,
            "Пожалуйста, пройдите регистрацию или войдите в свой аккаунт.\n"
            "Учтите, что после этого вы не сможете войти в другой аккаунт.",
            reply_markup=get_auth_request_kb(),
        )
        bot.delete_state(telegram_id, telegram_id)
        return None
    if state:
        bot.set_state(user_id=telegram_id, chat_id=telegram_id, state=state)
        with bot.retrieve_data(telegram_id, telegram_id) as data:
            data[TOKEN_KEY] = token
    return token
