from telebot import TeleBot
from telebot.types import CallbackQuery

from api.habits.delete_habit import delete_habit_by_id
from keyboards.inline.callback.enums import ActionsHabitEnum
from keyboards.inline.callback.factories import actions_with_habit_factory
from utils.constants import TOKEN_KEY
from utils.refresh_token import get_response_and_refresh_token


def delete_habit(callback: CallbackQuery, bot: TeleBot) -> None:
    number = int(actions_with_habit_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = get_response_and_refresh_token(
            telegram_id=callback.from_user.id,
            func=delete_habit_by_id,
            access_token=data[TOKEN_KEY],
            number=number - 1,
            data=data,
        )
    bot.answer_callback_query(
        callback_query_id=callback.id, text="Привычка успешно удалена!", show_alert=True
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
    )


def register_delete_habit(bot: TeleBot):
    bot.register_callback_query_handler(
        delete_habit,
        pass_bot=True,
        func=None,
        config=actions_with_habit_factory.filter(action=str(ActionsHabitEnum.DELETE)),
    )
