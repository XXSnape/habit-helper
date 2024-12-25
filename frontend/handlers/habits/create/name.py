from inline.keypads.cancel import get_cancel_kb
from states.habits import CreateHabitStates
from telebot import TeleBot
from telebot.types import Message
from utils.login_required import check_registration


def request_name(message: Message, bot: TeleBot) -> None:
    """
    Запрашивает название привычки
    :param message: Message
    :param bot: TeleBot
    """
    check_registration(message.chat.id, bot, state=CreateHabitStates.name)
    bot.send_message(
        message.chat.id, "Введите название для привычки", reply_markup=get_cancel_kb()
    )


def register_get_name(bot: TeleBot) -> None:
    """
    Регистрирует request_name
    :param bot: TeleBot
    """
    bot.register_message_handler(request_name, pass_bot=True, commands=["create_habit"])
