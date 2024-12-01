from telebot import TeleBot
from telebot.types import Message

from utils.refresh_token import get_response_and_refresh_token

from api.habits.my_habits import get_my_habits_by_token
from handlers.default.registration_error import check_registration


def get_my_habits(message: Message, bot: TeleBot):
    # bot.set_state(
    #     user_id=message.chat.id, chat_id=message.chat.id, state=HabitsStates.name
    # )
    token = check_registration(message.chat.id, bot)
    if token is False:
        return
    with bot.retrieve_data(message.chat.id, message.chat.id) as d:
        print(d)
    json = get_response_and_refresh_token(
        telegram_id=message.chat.id, func=get_my_habits_by_token, access_token=token
    )
    print("json", json)
    bot.send_message(message.chat.id, "Введите номер привычки для получения деталей")


def register_get_habits(bot: TeleBot):
    bot.register_message_handler(get_my_habits, pass_bot=True, commands=["my_habits"])
