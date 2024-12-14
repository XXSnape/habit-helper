from telebot import TeleBot
from telebot.types import Message, CallbackQuery


def unrecognized_message(message: Message, bot: TeleBot):
    bot.delete_state(message.chat.id, message.chat.id)
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n\n"
        "/start\n"
        "/create_habit\n"
        "/my_habits\n /log_in \n/change_password\n"
        "/my_info\n"
        "/completed_habits",
    )


def unrecognized_callback(callback: CallbackQuery, bot: TeleBot):
    bot.answer_callback_query(
        callback.id,
        text="Пожалуйста, введите запрос снова. Кнопка неактуальна сейчас.",
        show_alert=True,
    )
    bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)


def register_unrecognized_events(bot: TeleBot):
    bot.register_message_handler(unrecognized_message, pass_bot=True)
    bot.register_callback_query_handler(unrecognized_callback, pass_bot=True, func=None)
