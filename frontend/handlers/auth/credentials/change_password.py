from telebot import TeleBot
from telebot.types import Message

from handlers.default.registration_error import check_registration
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.auth import ChangePasswordStates
from utils.constants import MESSAGE_ID_KEY


def require_new_password(message: Message, bot: TeleBot):
    token = check_registration(
        message.chat.id, bot, state=ChangePasswordStates.password
    )
    if token is None:
        return
    sent_message = bot.send_message(
        message.chat.id, "Введите новый пароль", reply_markup=get_cancel_kb()
    )
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data[MESSAGE_ID_KEY] = sent_message.id


def register_require_new_password(bot: TeleBot):
    bot.register_message_handler(
        require_new_password, pass_bot=True, commands=["change_password"]
    )
