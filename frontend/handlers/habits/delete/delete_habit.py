from telebot import TeleBot
from telebot.types import CallbackQuery

from api.habits.delete_habit import delete_habit_by_number
from inline.callback.constants import MENU_OUTPUT
from inline.callback.enums import ActionsHabitEnum
from inline.callback.factories import actions_with_habit_factory
from inline.keypads.cancel import get_cancel_kb
from utils.cache_keys import TOKEN_KEY
from utils.refresh_token import get_response_and_refresh_token


def delete_habit(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Удаляет привычку на бэкэнде
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    number = int(actions_with_habit_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = get_response_and_refresh_token(
            telegram_id=callback.from_user.id,
            func=delete_habit_by_number,
            access_token=data[TOKEN_KEY],
            number=number,
            cache=data,
        )
    bot.answer_callback_query(
        callback_query_id=callback.id, text="Привычка успешно удалена!", show_alert=True
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text="Нет ни одной привычки" if text is None else text,
        reply_markup=get_cancel_kb(MENU_OUTPUT),
    )


def register_delete_habit(bot: TeleBot) -> None:
    """
    Регистрирует delete_habit
    :param bot: TeleBot
    """
    bot.register_callback_query_handler(
        delete_habit,
        pass_bot=True,
        func=None,
        config=actions_with_habit_factory.filter(action=str(ActionsHabitEnum.DELETE)),
    )
