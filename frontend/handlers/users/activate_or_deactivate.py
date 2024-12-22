from telebot import TeleBot
from telebot.types import CallbackQuery

from api.users.activity_user import activate_or_deactivate_user_by_flag
from utils.login_required import check_registration
from inline.callback.factories import activity_user_factory
from utils.refresh_token import get_response_and_refresh_token
from utils.texts import COMMANDS


def activate_or_deactivate_user(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Активирует или деактивирует пользователя. Неактивному пользователю не приходят напоминания о привычках.
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    token = check_registration(callback.from_user.id, bot)
    is_active = bool(int(activity_user_factory.parse(callback.data)["is_active"]))
    get_response_and_refresh_token(
        telegram_id=callback.from_user.id,
        func=activate_or_deactivate_user_by_flag,
        access_token=token,
        is_active=is_active,
    )
    message = (
        "Работа бота возобновлена! Ждите напоминаний!"
        if is_active
        else "Бот больше не будет присылать уведомления"
    )
    bot.answer_callback_query(
        callback_query_id=callback.id, text=message, show_alert=True
    )
    bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)
    bot.send_message(callback.from_user.id, text=COMMANDS)


def register_activate_or_deactivate(bot: TeleBot) -> None:
    """
    Регистрирует activate_or_deactivate_user
    :param bot: TeleBot
    """
    bot.register_callback_query_handler(
        activate_or_deactivate_user,
        pass_bot=True,
        func=None,
        config=activity_user_factory.filter(),
    )
