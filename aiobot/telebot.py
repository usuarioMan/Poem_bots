import logging
from aiogram import Bot, Dispatcher, executor, types
from os import environ

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from twitter.main import get_random_tweet_from_user

API_TOKEN = environ['TELBOT_TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(f'Hola soy el perrito poeta. Para un poema, escribe:  /p')


@dp.message_handler(commands=['p'])
async def dame_poema(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    tweet = await get_random_tweet_from_user('MicroPoesia')
    await message.answer(tweet)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    "🥳"