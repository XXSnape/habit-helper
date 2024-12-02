from telebot import TeleBot
from telebot.types import CallbackQuery
from telegram_bot_calendar import LSTEP

from keyboards.inline.callback.enums import ActionsHabitEnum
from keyboards.inline.callback.factories import (
    actions_with_habit_factory,
)
from utils.constants import HABITS_KEY
from utils.custom_calendar import CustomCalendar


def show_calendar(callback: CallbackQuery, bot: TeleBot):
    bot.send_message(callback.from_user.id, "hello")
    number = int(actions_with_habit_factory.parse(callback.data)["num_habit"]) - 1
    completed = set()
    not_completed = set()
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        for t in data[HABITS_KEY][number]["tracking"]:
            if t["is_done"] is True:
                completed.add(t["date"])
            else:
                not_completed.add(t["date"])

    calendar, step = CustomCalendar(
        completed=completed, not_completed=not_completed
    ).build()
    bot.send_message(
        callback.from_user.id, f"Select {LSTEP[step]}", reply_markup=calendar
    )


def register_calendar(bot: TeleBot):
    bot.register_callback_query_handler(
        show_calendar,
        pass_bot=True,
        func=None,
        config=actions_with_habit_factory.filter(action=str(ActionsHabitEnum.VIEW)),
    )
