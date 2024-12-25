from inline.callback.enums import ActionsHabitEnum
from inline.callback.factories import actions_with_habit_factory
from telebot import TeleBot
from telebot.types import CallbackQuery
from utils.cache_keys import (
    CONTEXT_KEY,
    HABITS_KEY,
    MAX_DATE_KEY,
    MIN_DATE_KEY,
    REASONS_KEY,
)
from utils.custom_calendar import (
    RU_LSTEP,
    CustomCalendar,
    get_completed_and_unfulfilled_dates,
)
from utils.output import get_date_designation
from utils.router_assistants.calendar import checking_habit_for_completion_by_date


def show_calendar(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Выводит календарь с датами, когда привычки были выполнены и не выполнены.
    :param callback: CallbackQuery
    :param bot: TeleBot

    """
    number = int(actions_with_habit_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        completed, not_completed = get_completed_and_unfulfilled_dates(
            number=number, data=data
        )
        if completed is None:
            bot.answer_callback_query(
                callback_query_id=callback.id,
                text="Эта привычка пока ни разу не была отмечена",
                show_alert=True,
            )
            return

        data[CONTEXT_KEY] = number
        min_date = data[HABITS_KEY][number][MIN_DATE_KEY]
        max_date = data[HABITS_KEY][number][MAX_DATE_KEY]
        name = data[HABITS_KEY][number]["name"]
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
        text=f"{get_date_designation(name)}\n\nВыберите {RU_LSTEP[step]}:",
        reply_markup=calendar,
    )


def process_date_selection(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Обрабатывает нажатие на кнопку календаря.
    Перелистывает года, месяца, если пользователь выбирает дату.
    Показывает причину невыполнения, если пользователь нажал на дату, когда причина не была выполнена.
    Показывает сообщение об ошибке, если пользователь нажал на пустую кнопку
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        number = data[CONTEXT_KEY]
        completed, not_completed = get_completed_and_unfulfilled_dates(
            number=number, data=data
        )
        reasons = data[HABITS_KEY][number][REASONS_KEY]
        min_date = data[HABITS_KEY][number][MIN_DATE_KEY]
        max_date = data[HABITS_KEY][number][MAX_DATE_KEY]
        name = data[HABITS_KEY][number]["name"]
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
            f"{get_date_designation(name)}\n\nВыберите {RU_LSTEP[step]}:",
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


def register_calendar(bot: TeleBot) -> None:
    """
    Регистрирует show_calendar, process_date_selection
    :param bot: TeleBot
    """
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
