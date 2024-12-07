from telebot import TeleBot
from telebot.types import Message

from api.users.check_user import check_user_existence
from keyboards.inline.keypads.auth import delete_password_request_kb
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.auth import AuthStates
from utils.constants import USERNAME_KEY, MESSAGE_ID_KEY


def validate_username_and_request_password(message: Message, bot: TeleBot):
    username = message.text
    is_existing = check_user_existence(username)
    if is_existing:
        bot.send_message(
            message.chat.id,
            f"К сожалению, пользователь {username} уже существует. Напишите другой никнейм",
            reply_markup=get_cancel_kb(),
        )
        return
    message = bot.send_message(
        message.chat.id,
        f"Отлично! Ваш потенциальный никнейм: {username}. Теперь нужно ввести пароль.\n"
        f'После того, как я его приму, пожалуйста, нажмите на кнопку "удалить сообщение" и удалите пароль из переписки',
        reply_markup=delete_password_request_kb(),
    )
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data[USERNAME_KEY] = username
        data[MESSAGE_ID_KEY] = message.id
    bot.set_state(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state=AuthStates.password,
    )


def register_password(bot: TeleBot):
    bot.register_message_handler(
        validate_username_and_request_password, pass_bot=True, state=AuthStates.username
    )
