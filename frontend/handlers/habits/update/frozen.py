from telebot import TeleBot
from telebot.types import CallbackQuery

from api.habits.freeze_habit import freeze_habit_by_id
from database.crud.check_user import get_user_token
from inline.callback.enums import HabitPropertiesEnum
from inline.callback.factories import (
    opportunities_for_change_factory,
    freeze_habit_factory,
)
from utils.cache_keys import HABITS_KEY
from utils.router_assistants.update_habit import change_property_by_callback


def frozen_habit_on_notification(callback: CallbackQuery, bot: TeleBot):
    habit_id = int(freeze_habit_factory.parse(callback.data)["habit_id"])
    token = get_user_token(telegram_id=callback.from_user.id)
    freeze_habit_by_id(access_token=token, habit_id=habit_id)
    bot.answer_callback_query(
        callback_query_id=callback.id,
        text="Привычка успешно приостановлена. Бот пока не будет отправлять о ней напоминания.",
        show_alert=True,
    )
    bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)


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
            property=str(HabitPropertiesEnum.IS_FROZEN)
        ),
    )
    bot.register_callback_query_handler(
        frozen_habit_on_notification,
        pass_bot=True,
        func=None,
        config=freeze_habit_factory.filter(),
    )
