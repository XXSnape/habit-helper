from telebot import TeleBot
from telebot.types import Message

from database.crud.check_user import get_user_token
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.auth import LogInStates


def log_in_to_another_account(message: Message, bot: TeleBot):
    token = get_user_token()
    bot.set_state(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state=LogInStates.username,
    )
    bot.send_message(
        message.chat.id,
        "Введите ник, чтобы войти другой аккаунт",
        reply_markup=get_cancel_kb(),
    )


def register_log_in_username(bot: TeleBot):
    bot.register_message_handler(
        log_in_to_another_account, commands=["log_in"], pass_bot=True
    )
