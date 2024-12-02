from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.inline.buttons.habits import edit_habits_factory
from keyboards.inline.keypads.habits import get_properties_to_change_kb


def provide_with_choosing_to_change(callback: CallbackQuery, bot: TeleBot):
    callback_data: dict = edit_habits_factory.parse(callback_data=callback.data)
    number = callback_data["num_habit"]
    with bot.retrieve_data(callback.from_user.id, callback.from_user.id) as data:
        text = data[number]
    text = f"<b>Выберете атрибут для изменения</b>\n\n{text}"
    bot.edit_message_text(
        message_id=callback.message.id,
        chat_id=callback.message.chat.id,
        text=text,
        reply_markup=get_properties_to_change_kb(number),
    )


def register_provide_with_choosing(bot: TeleBot):
    bot.register_callback_query_handler(
        provide_with_choosing_to_change,
        pass_bot=True,
        func=None,
        config=edit_habits_factory.filter(),
    )
