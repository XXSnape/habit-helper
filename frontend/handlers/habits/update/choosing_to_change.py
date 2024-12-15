from telebot import TeleBot
from telebot.types import CallbackQuery

from inline.callback.enums import ActionsHabitEnum
from inline.callback.factories import actions_with_habit_factory
from inline.keypads.habits import get_properties_to_change_kb
from utils.cache_keys import HABITS_KEY
from utils.output import get_habit_details_from_cache


def provide_with_choosing_to_change(callback: CallbackQuery, bot: TeleBot):
    callback_data: dict = actions_with_habit_factory.parse(callback_data=callback.data)
    number = int(callback_data["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = get_habit_details_from_cache(
            data=data, number=number, initial_text="Выберете атрибут для изменения"
        )
        is_frozen = data[HABITS_KEY][number]["is_frozen"]
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_properties_to_change_kb(number, iz_frozen=is_frozen),
    )


def register_provide_with_choosing(bot: TeleBot):
    bot.register_callback_query_handler(
        provide_with_choosing_to_change,
        pass_bot=True,
        func=None,
        config=actions_with_habit_factory.filter(action=str(ActionsHabitEnum.EDIT)),
    )
