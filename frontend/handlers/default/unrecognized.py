from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from utils.texts import COMMANDS


def unrecognized_message(message: Message, bot: TeleBot):
    bot.delete_state(message.chat.id, message.chat.id)
    bot.send_message(
        message.chat.id,
        text=COMMANDS,
    )


def unrecognized_callback(callback: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(
        callback.id,
        text="Пожалуйста, введите запрос снова. Кнопка неактуальна сейчас.",
        show_alert=True,
    )
    bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)
    bot.send_message(callback.from_user.id, text=COMMANDS)


def register_unrecognized_events(bot: TeleBot):
    bot.register_message_handler(unrecognized_message, pass_bot=True)
    bot.register_callback_query_handler(unrecognized_callback, pass_bot=True, func=None)
