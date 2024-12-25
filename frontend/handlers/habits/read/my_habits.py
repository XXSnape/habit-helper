from api.habits.my_habits import get_my_habits_by_token
from inline.callback.callbacks import MY_HABITS_CALLBACK
from inline.callback.constants import MENU_OUTPUT
from inline.keypads.cancel import get_cancel_kb
from states.habits import ReadHabitStates
from telebot import TeleBot
from telebot.types import CallbackQuery, Message
from utils.cache_keys import COMPLETED_KEY
from utils.login_required import check_registration
from utils.output import get_text_from_cache
from utils.refresh_token import get_response_and_refresh_token


def get_my_habits_by_command(message: Message, bot: TeleBot) -> None:
    """
    Выводит номера в кэше и названия привычек пользователя по командам /my_habits, /completed_habits
    при вводе /my_habits выводятся действующие привычки, иначе завершённые
    :param message: Message
    :param bot: TeleBot
    """
    token = check_registration(message.chat.id, bot, state=ReadHabitStates.details)
    is_complete_null = message.text == "/my_habits"
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        text = get_response_and_refresh_token(
            telegram_id=message.chat.id,
            func=get_my_habits_by_token,
            access_token=token,
            cache=data,
            is_complete_null=is_complete_null,
        )
        data[COMPLETED_KEY] = is_complete_null
    if text is None:
        bot.send_message(
            message.chat.id,
            "Нет ни одной привычки.",
            reply_markup=get_cancel_kb(MENU_OUTPUT),
        )
        return
    bot.send_message(message.chat.id, text, reply_markup=get_cancel_kb(MENU_OUTPUT))


def get_my_habits_by_callback(callback: CallbackQuery, bot: TeleBot) -> None:
    """
    Выводит номера в кэше и названия привычек пользователя по нажатию на кнопку
    :param callback: CallbackQuery
    :param bot: TeleBot
    """
    bot.set_state(
        user_id=callback.from_user.id,
        chat_id=callback.from_user.id,
        state=ReadHabitStates.details,
    )
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = get_text_from_cache(data)
    if text is None:
        bot.edit_message_text(
            message_id=callback.message.id,
            chat_id=callback.message.chat.id,
            text="Нет ни одной привычки.",
            reply_markup=get_cancel_kb(MENU_OUTPUT),
        )
        return
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_cancel_kb(MENU_OUTPUT),
    )


def register_get_habits(bot: TeleBot) -> None:
    """
    Регистрирует get_my_habits_by_command
    :param bot: TeleBot
    """
    bot.register_message_handler(
        get_my_habits_by_command,
        pass_bot=True,
        commands=["my_habits", "completed_habits"],
    )
    bot.register_callback_query_handler(
        get_my_habits_by_callback,
        pass_bot=True,
        func=lambda c: c.data == MY_HABITS_CALLBACK,
    )
