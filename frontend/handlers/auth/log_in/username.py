from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from keyboards.inline.callback.callbacks import LOG_IN_CALLBACK
from states.auth import LogInStates
from utils.router_assistants.auth import ask_for_username


def log_in_to_another_account(callback: CallbackQuery, bot: TeleBot):
    ask_for_username(
        callback=callback,
        bot=bot,
        state=LogInStates.username,
    )
    # bot.set_state(
    #     user_id=callback.from_user.id,
    #     chat_id=callback.from_user.id,
    #     state=LogInStates.username,
    # )
    # bot.edit_message_text(
    #     message_id=callback.message.id,
    #     chat_id=callback.message.chat.id,
    #     text=f"Пожалуйста, введите никнейм для использования бота.",
    #     reply_markup=get_cancel_kb(),
    # )


def register_log_in_username(bot: TeleBot):
    bot.register_callback_query_handler(
        log_in_to_another_account,
        pass_bot=True,
        func=lambda clb: clb.data == LOG_IN_CALLBACK,
    )
