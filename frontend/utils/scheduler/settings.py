from apscheduler.schedulers.background import BackgroundScheduler
from telebot import TeleBot

from .tasks import send_reminders_to_all_users


def register_tasks(scheduler: BackgroundScheduler, bot: TeleBot):
    scheduler.add_job(
        send_reminders_to_all_users,
        "cron",
        hour="18",
        minute="*",
        kwargs={"bot": bot, "hour": 20},
    )
    # scheduler.add_job(
    #     send_reminders_to_all_users,
    #     "cron",
    #     hour="20",
    #     minute="*",
    #     kwargs={"bot": bot, "hour": 21},
    # )
    # for hour in range(23):
    #     scheduler.add_job(
    #         send_reminders_to_all_users,
    #         "cron",
    #         hour=f"{hour}",
    #         minute="0",
    #         kwargs={"bot": bot, "hour": hour},
    #     )
