from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from api.habits.update_habit import update_habit
from keyboards.inline.callback.enums import HabitProperties
from keyboards.inline.callback.factories import opportunities_for_change_factory
from keyboards.inline.keypads.habits import (
    get_back_to_action_kb,
    get_actions_with_habit_kb,
)
from states.habits import ChangeHabitStates, ReadHabitStates
from utils.constants import CONTEXT_KEY, HABITS_KEY, TOKEN_KEY
from utils.refresh_token import get_response_and_refresh_token


def request_new_count(
    callback: CallbackQuery,
    bot: TeleBot,
):
    number = int(opportunities_for_change_factory.parse(callback.data)["num_habit"]) - 1
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        data[CONTEXT_KEY] = number
        old_count = data[HABITS_KEY][number]["count"]
        done_count = len(data[HABITS_KEY][number]["tracking"])
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.from_user.id,
        state=ChangeHabitStates.count,
    )
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=f"Введите новое количество дней для отправления напоминаний (не меньше {done_count}) вместо {old_count}",
        reply_markup=get_back_to_action_kb(number),
    )


def change_count(message: Message, bot: TeleBot):
    new_count = int(message.text)
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        number = data[CONTEXT_KEY]
        done_count = len(data[HABITS_KEY][number]["tracking"])
        if new_count < done_count:
            bot.send_message(
                message.chat.id,
                f"Вы уже выполнили данную привычку {done_count} дней. Введите число больше",
                reply_markup=get_back_to_action_kb(number),
            )
            return
        text = get_response_and_refresh_token(
            telegram_id=message.chat.id,
            func=update_habit,
            access_token=data[TOKEN_KEY],
            number=number,
            new_data={"count": new_count},
            cache=data,
        )
    bot.set_state(
        chat_id=message.chat.id,
        user_id=message.chat.id,
        state=ReadHabitStates.details,
    )
    bot.send_message(
        message.chat.id, text=text, reply_markup=get_actions_with_habit_kb(number)
    )


def register_change_count(bot: TeleBot):
    bot.register_callback_query_handler(
        request_new_count,
        pass_bot=True,
        func=None,
        config=opportunities_for_change_factory.filter(
            property=str(HabitProperties.COUNT)
        ),
    )
    bot.register_message_handler(
        change_count, pass_bot=True, state=ChangeHabitStates.count, regexp=r"\d+"
    )
