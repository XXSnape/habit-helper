import logging

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery

logger = logging.getLogger(__name__)


def try_delete_message(
    bot: TeleBot,
    callback: CallbackQuery,
):
    try:
        bot.delete_message(
            chat_id=callback.from_user.id, message_id=callback.message.id
        )
    except ApiTelegramException:
        logger.error(
            "Сообщение %s уже не может быть удалено", callback.message.message_id
        )
