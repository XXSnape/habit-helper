from inline.keypads.cancel import get_cancel_kb
from states.habits import CreateHabitStates
from telebot import TeleBot
from telebot.types import Message
from utils.cache_keys import NAME_KEY

from states.habits import ChangeHabitStates


def request_count(message: Message, bot: TeleBot) -> None:
    """
    Запрашивает количество дней отслеживания привычки
    :param message: Message
    :param bot: TeleBot
    """
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data[NAME_KEY] = message.text
    bot.send_message(
        message.chat.id,
        "Введите количество дней для отправки напоминаний (психологи рекомендуют 21 день)",
        reply_markup=get_cancel_kb(),
    )
    bot.set_state(
        user_id=message.chat.id, chat_id=message.chat.id, state=CreateHabitStates.count
    )


def handle_invalid_count(message: Message, bot: TeleBot) -> None:
    """
    Обрабатывает невалидный ввод: если число за рамками от 1 до 365
    :param message: Message
    :param bot: TeleBot
    """
    bot.send_message(
        message.chat.id,
        "Количество дней для отправки должно быть от 1 до 365. Введите число снова.",
        reply_markup=get_cancel_kb(),
    )


def register_get_count(bot: TeleBot) -> None:
    """
    Регистрирует request_count, handle_invalid_count
    :param bot:
    """
    bot.register_message_handler(
        request_count, pass_bot=True, state=CreateHabitStates.name
    )
    bot.register_message_handler(
        handle_invalid_count,
        func=lambda msg: (msg.text.isdigit() and int(msg.text) in range(1, 366))
        is False,
        pass_bot=True,
        state=CreateHabitStates.count,
    )
    bot.register_message_handler(
        handle_invalid_count,
        func=lambda msg: (msg.text.isdigit() and int(msg.text) in range(1, 366))
                         is False,
        pass_bot=True,
        state=ChangeHabitStates.count,
    )

