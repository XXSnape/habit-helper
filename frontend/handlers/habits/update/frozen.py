from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.callback.enums import HabitProperties
from keyboards.inline.callback.factories import opportunities_for_change_factory
from utils.constants import HABITS_KEY
from utils.router_assistants.update_habit import change_property_by_callback


def change_frozen_property(callback: CallbackQuery, bot: TeleBot):
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        number = int(opportunities_for_change_factory.parse(callback.data)["num_habit"])
        is_frozen_now = data[HABITS_KEY][number]["is_frozen"]
        change_property_by_callback(
            callback=callback,
            bot=bot,
            message=f"Привычка успешно {"разморожена" if is_frozen_now else "заморожена"}!",
            new_data={"is_frozen": not is_frozen_now},
            data=data,
            number=number,
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
