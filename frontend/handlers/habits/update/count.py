from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from keyboards.inline.callback.enums import HabitProperties
from keyboards.inline.callback.factories import opportunities_for_change_factory
from keyboards.inline.keypads.habits import (
    get_back_to_action_kb,
)
from states.habits import ChangeHabitStates
from utils.constants import CONTEXT_KEY, HABITS_KEY
from utils.router_assistants.update_habit import (
    request_new_property,
    change_property_by_message,
)


def request_new_count(
    callback: CallbackQuery,
    bot: TeleBot,
):
    number = int(opportunities_for_change_factory.parse(callback.data)["num_habit"])
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        data[CONTEXT_KEY] = number
        old_count = data[HABITS_KEY][number]["count"]
        done_count = len(data[HABITS_KEY][number]["tracking"])

    request_new_property(
        callback=callback,
        bot=bot,
        new_state=ChangeHabitStates.count,
        message=f"Введите новое количество дней для отправления напоминаний (не меньше {done_count}) вместо {old_count}",
        number=number,
    )


def change_count(message: Message, bot: TeleBot):
    new_count = int(message.text)
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        number = data[CONTEXT_KEY]
        done_count = len(data[HABITS_KEY][number]["tracking"])
        if new_count <= done_count:
            bot.send_message(
                message.chat.id,
                f"Вы уже выполнили данную привычку {done_count} дней. Введите число больше",
                reply_markup=get_back_to_action_kb(number),
            )
            return
    change_property_by_message(message=message, bot=bot, key="count", is_integer=True)


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
