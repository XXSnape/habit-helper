from telebot import TeleBot
from telebot.types import Message

from database.crud.check_user import get_user_token
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.auth import AuthStates, LogInStates
from utils.constants import USERNAME_KEY, MESSAGE_ID_KEY


def get_password_to_login_to_another_account(message: Message, bot: TeleBot):
    token = get_user_token(message.chat.id)
    if token:
        bot.set_state(
            user_id=message.chat.id,
            chat_id=message.chat.id,
            state=LogInStates.confirmation,
        )
        bot.send_message(
            message.chat.id,
            "У вас уже есть профиль, привязанный к данному телеграм аккаунту.\n"
            "Вы уверены, что хотите войти в другой аккаунт и объединить данные?",
            reply_markup=...
        )
    bot.set_state(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state=LogInStates.password,
    )
    message = bot.send_message(
        message.chat.id, "Введите пароль", reply_markup=get_cancel_kb()
    )
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data[USERNAME_KEY] = message.text
        data[MESSAGE_ID_KEY] = message.id


def register_log_in_password(bot: TeleBot):
    bot.register_message_handler(
        get_password_to_login_to_another_account,
        state=LogInStates.username,
        pass_bot=True,
    )
