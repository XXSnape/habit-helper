from telebot import TeleBot
from telebot.types import Message

from handlers.default.registration_error import check_registration
from keyboards.inline.keypads.cancel import get_cancel_kb
from states.habits import CreateHabitStates
from utils.constants import TOKEN_KEY


def request_name(message: Message, bot: TeleBot):
    bot.set_state(
        user_id=message.chat.id, chat_id=message.chat.id, state=CreateHabitStates.name
    )
    token = check_registration(message.chat.id, bot)
    if token is None:
        return
    bot.send_message(
        message.chat.id, "Введите название для привычки", reply_markup=get_cancel_kb()
    )


def register_get_name(bot: TeleBot):
    bot.register_message_handler(request_name, pass_bot=True, commands=["create_habit"])
