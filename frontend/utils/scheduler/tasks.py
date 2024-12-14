import logging

from telebot import TeleBot
from api.habits.all_habits import get_habits_all_users_by_hour
from keyboards.inline.keypads.habits import get_opportunity_to_mark_habit_kb
from utils.exceptions import InvalidApiResponse

d = [f"202411{str(k).zfill(2)}" for k in range(1, 30)]

logger = logging.getLogger(__name__)


def send_reminders_to_all_users(bot: TeleBot, hour: int) -> None:
    # current_date = datetime.now().strftime("%Y%m%d")
    current_date = d.pop(0)
    # current_date = "20241214"
    try:
        habits = get_habits_all_users_by_hour(hour=hour)
        for habit in habits:
            bot.send_message(
                chat_id=habit["telegram_id"],
                text=f"Пришло время отчета о привычке: «{habit['name']}».\nПожалуйста, нажмите на кнопку ниже",
                reply_markup=get_opportunity_to_mark_habit_kb(
                    habit_id=habit["id"], date=current_date
                ),
            )
    except InvalidApiResponse as e:
        logger.error("Не удалось получить привычки: %s", str(e))
