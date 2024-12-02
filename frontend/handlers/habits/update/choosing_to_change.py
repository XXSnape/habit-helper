from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.callback.enums import ActionsHabitEnum
from keyboards.inline.callback.factories import actions_with_habit_factory
from keyboards.inline.keypads.habits import get_properties_to_change_kb
from utils.output import get_habit_details_from_cache


def provide_with_choosing_to_change(callback: CallbackQuery, bot: TeleBot):
    callback_data: dict = actions_with_habit_factory.parse(callback_data=callback.data)
    number = int(callback_data["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = get_habit_details_from_cache(
            data=data, number=number - 1, initial_text="Выберете атрибут для изменения"
        )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_properties_to_change_kb(number),
    )


def register_provide_with_choosing(bot: TeleBot):
    bot.register_callback_query_handler(
        provide_with_choosing_to_change,
        pass_bot=True,
        func=None,
        config=actions_with_habit_factory.filter(action=str(ActionsHabitEnum.EDIT)),
    )
