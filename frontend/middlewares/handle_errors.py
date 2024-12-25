import logging

from inline.callback.constants import MENU_OUTPUT
from inline.keypads.auth import get_auth_request_kb
from inline.keypads.cancel import get_cancel_kb
from telebot import BaseMiddleware, TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, Message
from utils.delete_message import try_delete_message
from utils.exceptions import InvalidApiResponse, TokenMissing


def handle_token_missing(bot: TeleBot, telegram_id: int) -> None:
    """
    Обрабатывает случай, когда пользователь с id telegram_id не найден в базе.
    В таком случае сбрасывается состояние
    и отправляется просьба выполнить вход или зарегистрироваться
    :param bot: TeleBot
    :param telegram_id: телеграм id
    """
    bot.send_message(
        telegram_id,
        "Пожалуйста, пройдите регистрацию или войдите в свой аккаунт.\n"
        "Учтите, что после этого вы не сможете войти в другой аккаунт.",
        reply_markup=get_auth_request_kb(),
    )
    bot.delete_state(telegram_id, telegram_id)


class HandleErrorsMiddleware(BaseMiddleware):
    """
    Обрабатывает возможные ошибки и логирует их
    """

    def __init__(self, bot: TeleBot) -> None:
        """
        Инициализация
        :param bot: TeleBot
        """
        super().__init__()
        self._bot = bot
        self.update_types = ["message", "callback_query"]
        self.update_sensitive = True
        self.logger = logging.getLogger(__name__)

    def pre_process_message(self, message: Message, data: dict) -> None:
        """
        Обрабатывает событие Message перед отправкой в хэндлеры
        :param message: Message
        :param data: дополнительные данные
        """
        self.logger.info(
            f"Получено новое сообщение с id %s от пользователя %s c id %s",
            message.id,
            message.from_user.first_name,
            message.from_user.id,
        )

    def post_process_message(
        self, message: Message, data: dict, exception=None
    ) -> None:
        """
        Обрабатывает событие Message после отработки хэндлера.
        В случае какого-либо исключения сбрасывает состояние пользователя
        и выводит информацию об ошибке
        :param message: Message
        :param data: дополнительные данные
        :param exception: возникшее исключение или None
        :return:
        """
        if exception:
            if isinstance(exception, TokenMissing):
                handle_token_missing(bot=self._bot, telegram_id=message.chat.id)
                return

            self.logger.error("Ошибка: %s", str(exception))
            self._bot.send_message(
                message.chat.id,
                text="Произошла ошибка. Пожалуйста, попробуйте позже.",
                reply_markup=get_cancel_kb(MENU_OUTPUT),
            )
            self._bot.delete_state(message.chat.id, message.chat.id)
            return
        self.logger.info(
            "Обработано сообщение с id %s от пользователя %s c id %s",
            message.id,
            message.from_user.first_name,
            message.from_user.id,
        )

    def pre_process_callback_query(self, callback: CallbackQuery, data: dict) -> None:
        """
        Обрабатывает событие CallbackQuery перед отправкой в хэндлер
        :param callback: CallbackQuery
        :param data: дополнительные данные
        """
        if callback.message:
            self.logger.info(
                "Получено callback с id %s "
                "от пользователя %s с id %s "
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
    ) -> None:
        """
        Обрабатывает событие CallbackQuery после отработки хэндлера.
        В случае какого-либо исключения сбрасывает состояние пользователя
        и выводит информацию об ошибке через всплывающее окно. Сообщение
        пользователю может передаваться через экземпляр исключения
        :param callback: CallbackQuery
        :param data: дополнительные данные
        :param exception: возникшее исключение или None
        """
        if exception:
            if isinstance(exception, TokenMissing):
                handle_token_missing(bot=self._bot, telegram_id=callback.from_user.id)
                return
            if isinstance(exception, InvalidApiResponse) and str(exception):
                text = str(exception)
            else:
                text = "Кнопка больше не актуальна, пожалуйста, сделайте запрос снова"
            self.logger.error("Ошибка %s", str(exception))
            self._bot.answer_callback_query(callback.id, text=text, show_alert=True)
            self._bot.delete_state(callback.from_user.id, callback.from_user.id)
            if isinstance(exception, ApiTelegramException) is False:
                try_delete_message(bot=self._bot, callback=callback)

        if callback.message:
            self.logger.info(
                "Обработано "
                "callback с id %s "
                "от пользователя %s с id %s "
                "на сообщение с id %s "
                "с данными %s",
                callback.id,
                callback.from_user.first_name,
                callback.from_user.id,
                callback.message.id,
                callback.data,
            )
