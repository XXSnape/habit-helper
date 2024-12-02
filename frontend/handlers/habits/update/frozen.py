from telebot import TeleBot
from telebot.types import CallbackQuery

from api.habits.update_habit import update_habit
from keyboards.inline.callback.enums import HabitProperties
from keyboards.inline.callback.factories import opportunities_for_change_factory
from keyboards.inline.keypads.habits import get_actions_with_habit_kb
from utils.constants import TOKEN_KEY, HABITS_KEY
from utils.refresh_token import get_response_and_refresh_token


def change_frozen_property(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        number = (
            int(opportunities_for_change_factory.parse(callback.data)["num_habit"]) - 1
        )
        is_frozen_now = data[HABITS_KEY][number]["is_frozen"]
        text = get_response_and_refresh_token(
            telegram_id=callback.from_user.id,
            func=update_habit,
            access_token=data[TOKEN_KEY],
            number=number,
            new_data={"is_frozen": not is_frozen_now},
            cache=data,
        )
    bot.answer_callback_query(
        callback_query_id=callback.id,
        text=f"Привычка успешно {"разморожена" if is_frozen_now else "заморожена"}!",
        show_alert=True,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_actions_with_habit_kb(number),
    )


def register_change_frozen(bot: TeleBot):
    bot.register_callback_query_handler(
        change_frozen_property,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitProperties.IS_FROZEN)
        ),
    )
