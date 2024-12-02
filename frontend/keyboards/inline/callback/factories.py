from telebot.callback_data import CallbackData

actions_with_habit_factory = CallbackData("num_habit", "action", prefix="actions")
opportunities_for_change_factory = CallbackData("num_habit", "property", prefix="edit")
