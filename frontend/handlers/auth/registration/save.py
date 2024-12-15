from telebot import TeleBot
from telebot.types import Message

from api.users.create_user import get_access_token_for_new_user
from states.auth import AuthStates
from utils.constants import USERNAME_KEY, MESSAGE_ID_KEY
from database.crud.add_user import add_new_user
from utils.regexp import PASSWORD_REGEXP
from utils.texts import COMMANDS, DELETE_PASSWORD


def save_user(message: Message, bot: TeleBot):
    password = message.text
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        username = data[USERNAME_KEY]
        message_id = data[MESSAGE_ID_KEY]
    access_token = get_access_token_for_new_user(
        username=username, password=password, telegram_id=message.chat.id
    )
    add_new_user(telegram_id=message.chat.id, access_token=access_token)
    bot.delete_state(message.chat.id, message.chat.id)
    bot.delete_message(message.chat.id, message_id)
    bot.send_message(
        message.chat.id,
        f"Регистрация прошла успешно!\n" f"{DELETE_PASSWORD}",
    )
    bot.send_message(message.chat.id, text=COMMANDS)


def register_saving_user(bot: TeleBot):
    bot.register_message_handler(
        save_user,
        pass_bot=True,
        state=AuthStates.password,
        regexp=PASSWORD_REGEXP,
    )
