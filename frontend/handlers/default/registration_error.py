from telebot import TeleBot

from database.crud.check_user import get_user_token
from keyboards.inline.keypads.auth import get_auth_request_kb
from utils.constants import TOKEN_KEY


def check_registration(telegram_id: int, bot: TeleBot) -> bool:
    print("check hello")
    token = get_user_token(telegram_id)
    if not token:
        bot.send_message(
            telegram_id,
            "Пожалуйста, пройдите регистрацию",
            reply_markup=get_auth_request_kb(),
        )
        bot.delete_state(telegram_id, telegram_id)
        return False
    with bot.retrieve_data(telegram_id, telegram_id) as data:
        data[TOKEN_KEY] = token
        return True
