from telebot import TeleBot
from telebot.types import Message

from api.habits.create_habit import create_new_habit
from states.habits import HabitsStates
from utils.constants import NAME_KEY, COUNT_KEY, HOUR_KEY, TOKEN_KEY


def save_habit_with_description(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        print("d", data)
        name = data[NAME_KEY]
        count = data[COUNT_KEY]
        hour = data[HOUR_KEY]
        token = data[TOKEN_KEY]
    result = create_new_habit(
        access_token=token, name=name, count=count, hour=hour, description=message.text
    )
    if result:
        bot.send_message(message.chat.id, "Привычка успешно добавлена!")
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, попробуйте позже.")
    bot.delete_state(user_id=message.chat.id)


def register_save_habit(bot: TeleBot):
    bot.register_message_handler(
        save_habit_with_description, pass_bot=True, state=HabitsStates.save
    )
