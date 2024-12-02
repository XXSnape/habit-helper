from telegram_bot_calendar import WMonthTelegramCalendar, DetailedTelegramCalendar
from calendar import monthrange

from telegram_bot_calendar.base import *


class CustomCalendar(WMonthTelegramCalendar):
    def __init__(
        self,
        completed: set[str],
        not_completed: set[str],
        calendar_id=0,
        current_date=None,
        additional_buttons=None,
        locale="en",
        min_date=None,
        max_date=None,
        telethon=False,
        **kwargs
    ):
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
        self.completed = completed
        self.not_completed = not_completed

    def _get_decorated_button(self, current_date: date):
        if str(current_date) in self.completed:
            return "🟢" + str(current_date.day)
        if str(current_date) in self.not_completed:
            return "🔴" + str(current_date.day)
        if current_date:
            return str(current_date.day)
        return self.empty_day_button

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
