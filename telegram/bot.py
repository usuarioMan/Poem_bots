import telebot

from twitter.main import random_tweet

TOKEN = "2034401859:AAE1Wykv2m-oubBwe9qP7RuLXG91Q2MXMRc"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    poema = random_tweet()
    bot.reply_to(message, f"Guau, Majo tengo un poema para ti 🐶\n\n {poema}")


bot.polling()
