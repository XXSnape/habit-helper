from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.callback.enums import ActionsHabitEnum
from keyboards.inline.callback.factories import (
    actions_with_habit_factory,
)
from utils.constants import (
    HABITS_KEY,
    CONTEXT_KEY,
    REASONS_KEY,
    MIN_DATE_KEY,
    MAX_DATE_KEY,
)
from utils.custom_calendar import (
    CustomCalendar,
    get_completed_and_unfulfilled_dates,
    RU_LSTEP,
)
from utils.router_assistants.calendar import checking_habit_for_completion_by_date


def show_calendar(callback: CallbackQuery, bot: TeleBot):
    number = int(actions_with_habit_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        completed, not_completed = get_completed_and_unfulfilled_dates(
            number=number, data=data
        )
        data[CONTEXT_KEY] = number
        min_date = data[HABITS_KEY][number][MIN_DATE_KEY]
        max_date = data[HABITS_KEY][number][MAX_DATE_KEY]
    calendar, step = CustomCalendar(
        completed=completed,
        not_completed=not_completed,
        number=number,
        min_date=min_date,
        max_date=max_date,
        current_date=min_date,
    ).build()
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=f"Выберите {RU_LSTEP[step]}",
        reply_markup=calendar,
    )


def process_date_selection(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        number = data[CONTEXT_KEY]
        completed, not_completed = get_completed_and_unfulfilled_dates(
            number=number, data=data
        )
        reasons = data[HABITS_KEY][number][REASONS_KEY]
        min_date = data[HABITS_KEY][number][MIN_DATE_KEY]
        max_date = data[HABITS_KEY][number][MAX_DATE_KEY]
    result, key, step = CustomCalendar(
        completed=completed,
        not_completed=not_completed,
        number=number,
        min_date=min_date,
        max_date=max_date,
        current_date=min_date,
    ).process(callback.data)
    if not result and key:
        bot.edit_message_text(
            f"Выберите {RU_LSTEP[step]}",
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=key,
        )
        return
    elif result:
        checking_habit_for_completion_by_date(
            bot=bot,
            callback=callback,
            result=result,
            completed=completed,
            reasons=reasons,
        )
    else:
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Эта кнопка лишь для отображения😁",
            show_alert=True,
        )


def register_calendar(bot: TeleBot):
    bot.register_callback_query_handler(
        show_calendar,
        pass_bot=True,
        func=None,
        config=actions_with_habit_factory.filter(action=str(ActionsHabitEnum.VIEW)),
    )
    bot.register_callback_query_handler(
        process_date_selection,
        func=CustomCalendar.func(),
        pass_bot=True,
    )
