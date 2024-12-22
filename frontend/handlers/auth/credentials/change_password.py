from telebot import TeleBot
from telebot.types import Message

from utils.login_required import check_registration
from inline.keypads.cancel import get_cancel_kb
from states.auth import ChangePasswordStates
from utils.cache_keys import MESSAGE_ID_KEY


def require_new_password(message: Message, bot: TeleBot) -> None:
    """
    Запрашивает новый пароль
    :param message: Message
    :param bot: TeleBot
    """
    check_registration(message.chat.id, bot, state=ChangePasswordStates.password)
    sent_message = bot.send_message(
        message.chat.id, "Введите новый пароль", reply_markup=get_cancel_kb()
    )
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data[MESSAGE_ID_KEY] = sent_message.id


def register_require_new_password(bot: TeleBot) -> None:
    """
    Регистрирует require_new_password
    :param bot: TeleBot

    """
    bot.register_message_handler(
        require_new_password, pass_bot=True, commands=["change_password"]
    )
