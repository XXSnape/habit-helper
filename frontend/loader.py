import telebot
from config import settings


bot = telebot.TeleBot(settings.bot.token, use_class_middlewares=True, parse_mode="HTML")
