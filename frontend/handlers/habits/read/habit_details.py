from telebot.types import Message

from keyboards.inline.keypads.habits import get_actions_with_habit_kb
from utils.output import get_habit_details_from_cache

from telebot import TeleBot

from states.habits import ReadHabitStates


def get_habit_details(message: Message, bot: TeleBot):
    number = message.text
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        text = get_habit_details_from_cache(data=data, number=number)
    if text is None:
        bot.send_message(
            message.chat.id, "Не нашлось номера с такой привычкой, попробуйте снова"
        )
        return
    bot.send_message(
        message.chat.id, text, reply_markup=get_actions_with_habit_kb(number)
    )


def register_get_habit_details(bot: TeleBot):
    bot.register_message_handler(
        get_habit_details, regexp=r"\d+", state=ReadHabitStates.details, pass_bot=True
    )
