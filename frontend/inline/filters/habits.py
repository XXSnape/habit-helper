from telebot import AdvancedCustomFilter
from telebot.callback_data import CallbackDataFilter
from telebot.types import CallbackQuery


class EditHabitCallbackFilter(AdvancedCustomFilter):
    key = "config"

    def check(self, callback: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=callback)
