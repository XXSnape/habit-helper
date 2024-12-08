from telebot.callback_data import CallbackData

actions_with_habit_factory = CallbackData("num_habit", "action", prefix="actions")
opportunities_for_change_factory = CallbackData("num_habit", "property", prefix="edit")
mark_habit_factory = CallbackData("habit_id", "date", "is_done", prefix="mark")
activity_user_factory = CallbackData("is_active", prefix="frozen")
