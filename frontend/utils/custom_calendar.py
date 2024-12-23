from telegram_bot_calendar import WMonthTelegramCalendar, DetailedTelegramCalendar
from calendar import monthrange

from telegram_bot_calendar.base import *

from inline.callback.callbacks import MY_HABITS_CALLBACK
from inline.callback.factories import (
    habit_details_factory,
)
from utils.cache_keys import (
    HABITS_KEY,
    IS_DONE_KEY,
    IS_NOT_DONE_KEY,
    REASONS_KEY,
    MIN_DATE_KEY,
    MAX_DATE_KEY,
)
from datetime import date, datetime

from utils.texts import UNMARKED_DATE, MARKED_DATE
from typing import override

RU_LSTEP = {"y": "год", "m": "месяц", "d": "день"}


class CustomCalendar(WMonthTelegramCalendar):
    """
    Кастомный календарь для отображения данных о выполнении привычек в сплывающих окнах
    и на кнопках
    """

    prev_button = "⬅️"
    next_button = "➡️"

    @override
    def __init__(
        self,
        completed: list[str],
        not_completed: list[str],
        number: int,
        calendar_id=0,
        current_date=None,
        additional_buttons=None,
        locale="ru",
        min_date=None,
        max_date=None,
        telethon=False,
        **kwargs
    ) -> None:
        """

        :param completed: список с датами, когда задание было выполнено
        :param not_completed: список с датами, когда задание не было выполнено
        :param number: номер привычки в кэше
        """
        if additional_buttons is None:
            additional_buttons = [
                {
                    "text": "Назад",
                    "callback_data": habit_details_factory.new(num_habit=number),
                },
                {
                    "text": "Все привычки",
                    "callback_data": MY_HABITS_CALLBACK,
                },
            ]
        if (
            isinstance(min_date, str)
            and isinstance(current_date, str)
            and isinstance(max_date, str)
        ):
            min_date = datetime.strptime(min_date, "%Y-%m-%d").date()
            max_date = datetime.strptime(max_date, "%Y-%m-%d").date()
            current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
        super(DetailedTelegramCalendar, self).__init__(
            calendar_id,
            current_date=current_date,
            additional_buttons=additional_buttons,
            locale=locale,
            min_date=min_date,
            max_date=max_date,
            is_random=False,
            telethon=telethon,
            **kwargs
        )
        self.days_of_week["ru"] = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        self.completed = completed
        self.not_completed = not_completed

    def _get_decorated_button(self, current_date: date) -> str:
        """
        Изменяет отображение кнопки для пользователя.
        Делает кнопку зелёной, если в эту дату задание было выполнено, иначе красной.
        Если нет данных, то оставляет просто дату
        :param current_date: текущая рассматриваемая дата
        :return: кнопка с обновленным дизайном
        """
        if str(current_date) in self.completed:
            return MARKED_DATE + str(current_date.day)
        if str(current_date) in self.not_completed:
            return UNMARKED_DATE + str(current_date.day)
        if current_date:
            return str(current_date.day)
        return self.empty_day_button

    @override
    def _build_days(self, *args, **kwargs):
        days_num = monthrange(self.current_date.year, self.current_date.month)[1]

        start = self.current_date.replace(day=1)
        days = self._get_period(DAY, start, days_num)

        days_buttons = rows(
            [
                self._build_button(
                    self._get_decorated_button(d),
                    SELECT if d else NOTHING,
                    DAY,
                    d,
                    is_random=self.is_random,
                )
                for d in days
            ],
            self.size_day,
        )

        days_of_week_buttons = [
            [
                self._build_button(self.days_of_week[self.locale][i], NOTHING)
                for i in range(7)
            ]
        ]

        # mind and maxd are swapped since we need maximum and minimum days in the month
        # without swapping next page can generated incorrectly
        nav_buttons = self._build_nav_buttons(
            DAY,
            diff=relativedelta(months=1),
            maxd=max_date(start, MONTH),
            mind=min_date(start + relativedelta(days=days_num - 1), MONTH),
        )

        self._keyboard = self._build_keyboard(
            days_of_week_buttons + days_buttons + nav_buttons
        )

        # if self.telethon:
        #     return Button.inline(text=str(text), data=self._build_callback(action, step, data, is_random=is_random))
        # else:
        #     return {
        #         'text': text,
        #         'callback_data': self._build_callback(action, step, data, is_random=is_random)
        #     }


def get_completed_and_unfulfilled_dates(
    number: int, data: dict
) -> tuple[list[str], list[str]] | tuple[None, None]:
    """
    Получает даты, когда задание было выполнено и не выполнено, если они есть в кэше.
    Если данных нет, собирает их, добавляет в кэш причины, минимальные и максимальные даты

    :param number: номер привычки в кэше
    :param data: кэш
    :return: даты, когда задание было выполнено и не выполнено
    или None, None, если привычка ни разу не была отмечена
    """
    try:
        return (
            data[HABITS_KEY][number][IS_DONE_KEY],
            data[HABITS_KEY][number][IS_NOT_DONE_KEY],
        )
    except KeyError:
        reasons = {}
        is_done_habits = []
        is_not_done_habits = []
        min_date = datetime.now().date()
        max_date = None
        if len(data[HABITS_KEY][number]["tracking"]) == 0:
            return None, None
        for tracking in data[HABITS_KEY][number]["tracking"]:
            current_date = tracking["date"]
            if tracking["is_done"] is True:
                is_done_habits.append(current_date)
            else:
                is_not_done_habits.append(current_date)
                reasons[current_date] = tracking["reason"]
            min_date = min(min_date, datetime.strptime(current_date, "%Y-%m-%d").date())
            if max_date is None:
                max_date = datetime.strptime(current_date, "%Y-%m-%d").date()
            else:
                max_date = max(
                    max_date, datetime.strptime(current_date, "%Y-%m-%d").date()
                )
        data[HABITS_KEY][number].update(
            {
                IS_DONE_KEY: is_done_habits,
                IS_NOT_DONE_KEY: is_not_done_habits,
                REASONS_KEY: reasons,
                MIN_DATE_KEY: str(min_date),
                MAX_DATE_KEY: str(max_date),
            }
        )
        return is_done_habits, is_not_done_habits
