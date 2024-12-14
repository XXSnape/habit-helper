from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from api.habits.mark_habit import mark_habit
from database.crud.check_user import get_user_token
from keyboards.inline.callback.callbacks import REJECTION_REASON_CALLBACK
from keyboards.inline.callback.factories import mark_habit_factory
from keyboards.inline.keypads.habits import get_reason_waiver_kb
from states.habits import MarkHabitStates
from utils.constants import MARK_KEY, MESSAGE_ID_KEY
from utils.refresh_token import get_response_and_refresh_token
from utils.router_assistants.mark import get_data_on_completion_habit
from utils.texts import TASK_WAS_NOT_COMPLETED_TEXT


def successful_implementation_habit(callback: CallbackQuery, bot: TeleBot):
    is_the_end = get_data_on_completion_habit(callback=callback)
    bot.delete_state(callback.from_user.id, callback.from_user.id)
    if is_the_end:
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Поздравляю! Вы выполнили план! Надеюсь, вы добились желаемого прогресса.\n"
            "Если хотите, вы можете возобновить данную привычку",
            show_alert=True,
        )
    else:
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Вы успешно выполнили задачу! Продолжайте в том же духе!",
            show_alert=True,
        )
    bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)


def breaking_habit(callback: CallbackQuery, bot: TeleBot):
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.message.chat.id,
        state=MarkHabitStates.reason,
    )
    save_data = mark_habit_factory.parse(callback.data)
    save_data.pop("@")
    bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)
    sent_message = bot.send_message(
        callback.message.chat.id,
        text="Пожалуйста, укажите причину, по которой у вас не получилось выполнить задачу."
        " Это в дальнейшем поможет для анализа ошибок.",
        reply_markup=get_reason_waiver_kb(),
    )
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        data[MARK_KEY] = save_data
        data[MESSAGE_ID_KEY] = sent_message.id


def reason_is_not_specified(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        habit_data = data[MARK_KEY]
    token = get_user_token(callback.from_user.id)
    get_response_and_refresh_token(
        telegram_id=callback.from_user.id,
        func=mark_habit,
        access_token=token,
        **habit_data,
    )
    bot.delete_state(callback.from_user.id, callback.from_user.id)
    bot.answer_callback_query(
        callback_query_id=callback.id,
        text=TASK_WAS_NOT_COMPLETED_TEXT,
        show_alert=True,
    )
    bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)


def reason_is_specified(message: Message, bot: TeleBot):
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        habit_data = data[MARK_KEY]
        last_message_id = data[MESSAGE_ID_KEY]
    habit_data["reason"] = message.text
    token = get_user_token(message.chat.id)
    get_response_and_refresh_token(
        telegram_id=message.chat.id,
        func=mark_habit,
        access_token=token,
        **habit_data,
    )
    bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
    bot.delete_state(message.chat.id, message.chat.id)
    bot.send_message(message.chat.id, text=TASK_WAS_NOT_COMPLETED_TEXT)


def reason_text_is_too_large(message: Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        "Слишком длинный текст. Попробуйте снова",
        reply_markup=get_reason_waiver_kb(),
    )


def register_mark_habit(bot: TeleBot):
    bot.register_callback_query_handler(
        successful_implementation_habit,
        pass_bot=True,
        func=None,
        config=mark_habit_factory.filter(is_done="1"),
    )
    bot.register_callback_query_handler(
        breaking_habit,
        pass_bot=True,
        func=None,
        config=mark_habit_factory.filter(is_done="0"),
    )
    bot.register_callback_query_handler(
        reason_is_not_specified,
        state=MarkHabitStates.reason,
        pass_bot=True,
        func=lambda c: c.data == REJECTION_REASON_CALLBACK,
    )
    bot.register_message_handler(
        reason_is_specified,
        state=MarkHabitStates.reason,
        pass_bot=True,
        func=lambda m: len(m.text) < 150,
    )
    bot.register_message_handler(
        reason_text_is_too_large,
        state=MarkHabitStates.reason,
        pass_bot=True,
    )
