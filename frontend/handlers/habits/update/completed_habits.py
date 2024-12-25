from api.habits.resume_habit import resume_completed_habit
from inline.callback.enums import ActionsHabitEnum
from inline.callback.factories import actions_with_habit_factory
from inline.keypads.habits import (
    get_back_to_habits_details_and_menu,
    get_back_to_habits_kb,
)
from states.habits import ReadHabitStates, ResumeHabitStates
from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from utils.cache_keys import CONTEXT_KEY, HABITS_KEY, TOKEN_KEY
from utils.refresh_token import get_response_and_refresh_token


def require_new_count(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Запрашивает новое количество дней привития для возобновления, большее старого
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    number = int(actions_with_habit_factory.parse(callback.data)["num_habit"])
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.from_user.id,
        state=ResumeHabitStates.resume,
    )
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        data[CONTEXT_KEY] = number
        name = data[HABITS_KEY][number]["name"]
        count = data[HABITS_KEY][number]["count"]
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=f"Введите число напоминаний для привычки «{name}» большее {count}",
        reply_markup=get_back_to_habits_details_and_menu(number),
    )


def resume_habit(message: Message, bot: TeleBot) -> None:
    """
    Возобновляет привычку, если количество для привития больше старого, или выводит ошибку
    :param message: Message
    :param bot: TeleBot
    """
    new_count = int(message.text)
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        token = data[TOKEN_KEY]
        number = data[CONTEXT_KEY]
        done_count = data[HABITS_KEY][number]["count"]
        habit_id = data[HABITS_KEY][number]["id"]
        if new_count <= done_count:
            bot.send_message(
                message.chat.id,
                f"Вы уже выполнили данную привычку {done_count} дней. Введите число больше",
                reply_markup=get_back_to_habits_details_and_menu(number),
            )
            return
        data[HABITS_KEY].pop(number)
    get_response_and_refresh_token(
        telegram_id=message.chat.id,
        func=resume_completed_habit,
        access_token=token,
        habit_id=habit_id,
        count=new_count,
    )
    bot.set_state(
        user_id=message.chat.id,
        chat_id=message.chat.id,
        state=ReadHabitStates.details,
    )
    bot.send_message(
        message.chat.id,
        "Привычка успешно возобновлена!",
        reply_markup=get_back_to_habits_kb(),
    )


def register_resume_habits(bot: TeleBot) -> None:
    """
    Регистрирует require_new_count, resume_habit
    :param bot: TeleBot
    """
    bot.register_callback_query_handler(
        require_new_count,
        pass_bot=True,
        func=None,
        config=actions_with_habit_factory.filter(action=str(ActionsHabitEnum.RESUME)),
    )
    bot.register_message_handler(
        resume_habit, pass_bot=True, regexp=r"\d+", state=ResumeHabitStates.resume
    )
