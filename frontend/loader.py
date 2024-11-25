import telebot
from config import settings


bot = telebot.TeleBot(settings.bot.token)
