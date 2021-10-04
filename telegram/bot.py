import asyncio
from os import environ
import telebot

from twitter.main import get_random_tweet_from_user

TOKEN = environ['TELBOT_TOKEN']
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"Guau, Majo tengo algunos poema para ti 🐶\n\n Escribe: /poema")


@bot.message_handler(commands=['poema'])
def enviar_poema(message):
    poema = await get_random_tweet_from_user('MicroPoesia')
    bot.reply_to(message, poema)


bot.polling()
