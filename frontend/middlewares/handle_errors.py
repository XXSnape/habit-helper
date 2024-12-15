import logging

from telebot import BaseMiddleware, TeleBot
from telebot.types import CallbackQuery, Message

from inline.callback.constants import MENU_OUTPUT
from inline.keypads.cancel import get_cancel_kb
from utils.delete_message import try_delete_message
from utils.exceptions import InvalidApiResponse

HANDLED_STR = "Необработанно", "Обработано"


class HandleErrorsMiddleware(BaseMiddleware):

    def __init__(self, bot: TeleBot, logger=__name__):
        super().__init__()
        self._bot = bot
        self.update_types = ["message", "callback_query"]
        self.update_sensitive = True
        self.logger = logging.getLogger(logger)

    def pre_process_message(self, message: Message, data: dict):
        self.logger.debug(
            f"Получено новое сообщение с id %s от пользователя %s c id %s",
            message.id,
            message.from_user.first_name,
            message.from_user.id,
        )

    def post_process_message(self, message: Message, data: dict, exception=None):
        if exception:
            self.logger.error("Ошибка: %s", str(exception))
            self._bot.send_message(
                message.chat.id,
                text="Произошла ошибка. Пожалуйста, попробуйте позже.",
                reply_markup=get_cancel_kb(MENU_OUTPUT),
            )
            self._bot.delete_state(message.chat.id, message.chat.id)
            return
        self.logger.debug(
            f"%s " f"сообщение с id %s от пользователя %s c id %s",
            HANDLED_STR[bool(len(data))],
            message.id,
            message.from_user.first_name,
            message.from_user.id,
        )

    def pre_process_callback_query(self, callback: CallbackQuery, data: dict):
        if callback.message:
            self.logger.debug(
                "Получено callback с id %s "
                "от пользователя %s с id %s"
                "на сообщение с id %s"
                "с данными %s",
                callback.id,
                callback.from_user.first_name,
                callback.from_user.id,
                callback.message.id,
                callback.data,
            )

    def post_process_callback_query(
        self, callback: CallbackQuery, data, exception=None
    ):

        if exception:
            if isinstance(exception, InvalidApiResponse) and str(exception):
                text = str(exception)
            else:
                text = "Кнопка больше не актуальна, пожалуйста, сделайте запрос снова"
            self.logger.error("Ошибка %s", str(exception))
            self._bot.answer_callback_query(callback.id, text=text, show_alert=True)
            self._bot.delete_state(callback.from_user.id, callback.from_user.id)
            try_delete_message(bot=self._bot, callback=callback)

        if callback.message:
            self.logger.debug(
                f"%s "
                "callback с id %s "
                "от пользователя %s с id %s "
                "на сообщение с id %s "
                "с данными %s",
                HANDLED_STR[bool(len(data))],
                callback.id,
                callback.from_user.first_name,
                callback.from_user.id,
                callback.message.id,
                callback.data,
            )
