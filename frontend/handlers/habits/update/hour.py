from telebot import TeleBot
from telebot.types import CallbackQuery

from api.habits.update_habit import update_habit
from keyboards.inline.callback.enums import HabitProperties
from keyboards.inline.callback.factories import opportunities_for_change_factory
from keyboards.inline.keypads.habits import get_actions_with_habit_kb
from keyboards.inline.keypads.time import get_hour_selection_and_back_kb
from states.habits import ChangeHabitStates, ReadHabitStates
from utils.constants import HABITS_KEY, CONTEXT_KEY, TOKEN_KEY
from utils.refresh_token import get_response_and_refresh_token


def request_new_time(callback: CallbackQuery, bot: TeleBot):
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.from_user.id,
        state=ChangeHabitStates.hour,
    )
    number = int(opportunities_for_change_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        last_time = (
            f"{str(data[HABITS_KEY][number - 1]['notification_hour']).zfill(2)}:00"
        )
        data[CONTEXT_KEY] = number - 1
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=f"Выберете другое время, вместо {last_time}",
        reply_markup=get_hour_selection_and_back_kb(number),
    )


def change_time(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        number = data[CONTEXT_KEY]
        text = get_response_and_refresh_token(
            telegram_id=callback.from_user.id,
            func=update_habit,
            access_token=data[TOKEN_KEY],
            number=number,
            new_data={"notification_hour": int(callback.data)},
            cache=data,
        )
    bot.set_state(
        chat_id=callback.from_user.id,
        user_id=callback.from_user.id,
        state=ReadHabitStates.details,
    )
    bot.answer_callback_query(
        callback_query_id=callback.id,
        text="Привычка успешно обновлена!",
        show_alert=True,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_actions_with_habit_kb(number),
    )


def register_change_time(bot: TeleBot):
    bot.register_callback_query_handler(
        request_new_time,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitProperties.HOUR)
        ),
    )
    bot.register_callback_query_handler(
        change_time, pass_bot=True, func=None, state=ChangeHabitStates.hour
    )
