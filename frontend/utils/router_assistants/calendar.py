from datetime import date

from telebot import TeleBot
from telebot.types import CallbackQuery


def checking_habit_for_completion_by_date(
    bot: TeleBot,
    callback: CallbackQuery,
    result: date,
    completed: list[str],
    reasons: dict[str, str],
):
    date_string = str(result)
    if date_string in completed:
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Вы успешно выполнили всё в этот день! Продолжайте в том же духе!",
            show_alert=True,
        )
    try:
        reason = reasons[date_string]
        if reason is None:
            message = "К сожалению, вы не выполнили задуманное в этот день и не указали причину для отчётности."
        else:
            message = f"Указанная причина невыполнения:\n {reason}"
    except KeyError:
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="В этот день вы ничего не отмечали",
            show_alert=True,
        )
        return
    bot.answer_callback_query(
        callback_query_id=callback.id,
        text=message,
        show_alert=True,
    )
    return
