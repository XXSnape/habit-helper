from telebot import TeleBot
from telebot.types import Message

from api.users.change_password import change_password_by_token
from states.auth import ChangePasswordStates
from utils.constants import TOKEN_KEY, MESSAGE_ID_KEY
from utils.refresh_token import get_response_and_refresh_token
from utils.regexp import PASSWORD_REGEXP
from utils.texts import COMMANDS, DELETE_PASSWORD


def save_password(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        get_response_and_refresh_token(
            telegram_id=message.chat.id,
            func=change_password_by_token,
            access_token=data[TOKEN_KEY],
            password=message.text,
            tg_id=message.chat.id,
        )
        last_message_id = data[MESSAGE_ID_KEY]
    bot.delete_state(message.chat.id, message.chat.id)
    bot.delete_message(message.chat.id, last_message_id)
    bot.send_message(
        message.chat.id,
        f"Вы успешно сменили пароль!\n{DELETE_PASSWORD}",
    )
    bot.send_message(message.chat.id, text=COMMANDS)


def register_save_password(bot: TeleBot):
    bot.register_message_handler(
        save_password,
        pass_bot=True,
        state=ChangePasswordStates.password,
        regexp=PASSWORD_REGEXP,
    )
