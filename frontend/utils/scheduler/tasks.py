from datetime import datetime

from telebot import TeleBot

from api.habits.all_habits import get_habits_all_users_by_hour
from keyboards.inline.keypads.habits import get_opportunity_to_mark_habit_kb


def send_reminders_to_all_users(bot: TeleBot, hour: int) -> None:
    current_date = datetime.now().strftime("%Y%m%d")
    habits = get_habits_all_users_by_hour(hour=hour)
    for habit in habits:
        bot.send_message(
            chat_id=habit["telegram_id"],
            text=f"Пришло время отчета о привычке: «{habit['name']}».\nПожалуйста, нажмите на кнопку ниже",
            reply_markup=get_opportunity_to_mark_habit_kb(
                habit_id=habit["id"], date=current_date
            ),
        )
