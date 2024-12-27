from apscheduler.schedulers.background import BackgroundScheduler
from telebot import TeleBot

from .tasks import send_reminders_to_all_users


def register_tasks(scheduler: BackgroundScheduler, bot: TeleBot) -> None:
    """
    Регистрирует задачи по отправлению напоминаний пользователю о ежедневных привычках.
    Каждый час будет происходить проверка на то, нужно ли отправлять кому-то напоминание
    :param scheduler: BackgroundScheduler
    :param bot: TeleBot
    :return:
    """
    for hour in range(23):
        scheduler.add_job(
            send_reminders_to_all_users,
            "cron",
            hour=f"{hour}",
            minute="0",
            kwargs={"bot": bot, "hour": hour},
        )
