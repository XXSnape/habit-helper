from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from api.users.create_user import create_user
from keyboards.inline.callback.callbacks import REGISTRATION_CALLBACK
from keyboards.inline.keypads.auth import delete_password_request_kb
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.auth import AuthStates
from api.users.check_user import check_user_existence
from utils.constants import USERNAME_KEY, MESSAGE_ID_KEY


def request_username(callback: CallbackQuery, bot: TeleBot):
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.message.chat.id,
        state=AuthStates.username,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=f"Пожалуйста, введите никнейм для использования бота.",
        reply_markup=get_cancel_kb(),
    )


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


def save_user(message: Message, bot: TeleBot):
    password = message.text
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        username = data[USERNAME_KEY]
        message_id = data[MESSAGE_ID_KEY]
    access_token = create_user(
        username=username, password=password, telegram_id=message.chat.id
    )
    print("token", access_token)
    bot.delete_message(message.chat.id, message_id)
    bot.send_message(message.chat.id, "delete your")


def register_auth_user(bot: TeleBot):
    bot.register_callback_query_handler(
        request_username,
        pass_bot=True,
        func=lambda clb: clb.data == REGISTRATION_CALLBACK,
    )
    bot.register_message_handler(
        validate_username_and_request_password, pass_bot=True, state=AuthStates.username
    )
    bot.register_message_handler(save_user, pass_bot=True, state=AuthStates.password)
