import asyncio
import random
import tweepy
from os import environ

from db.utils import get_motor_client

consumer_key = environ['CONSUMER_KEY']
consumer_secret = environ['CONSUMER_SECRET']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def fetch_user(screen, as_dict=True):
    if as_dict:
        user = api.get_user(screen_name=screen)
        return user._json

    else:
        user = api.get_user(screen_name=screen)
        return user


def fetch_id(screen):
    user = api.get_user(screen_name=screen)
    return user.id


def fetch_ids(list_screens):
    ids = [fetch_id(name) for name in list_screens]
    return ids


def random_tweet():
    poemas = list()
    for tweet in api.user_timeline(user_id="14186744"):
        poemas.append(tweet.text)

    return random.choice(poemas)


async def save_user_to_db(user_json):
    client = get_motor_client()
    cuentas = client.get_collection('perrito_poeta', 'cuentas_twitter')
    await cuentas.insert_one(user_json)


async def save_user_from_screen_to_db(screen_name):
    user = fetch_user(screen_name)
    await save_user_to_db(user)


async def fetch_all_statuses():
    """
    Obtiene todas las observaciones de la base de datos.
    Busca todos los tweets disponibles para todos los usuarios.
    """
    client = get_motor_client()
    collection = client.get_collection('perrito_poeta', 'cuentas_twitter')

    id_strings = list()
    async for cuenta in collection.find({}):
        id_strings.append(cuenta['id_str'])

    for id_str in id_strings:
        result_set = api.user_timeline(user_id=id_str)
        tweets = [tweet._json for tweet in result_set]
        for tweet in tweets:
            await collection.update_one({'id_str': id_str}, {"$addToSet": {"tweets": tweet}})
            print(tweet)


async def get_user_by_screen_name(screen_name):
    client = get_motor_client()
    collection = client.get_collection('perrito_poeta', 'cuentas_twitter')
    user = await collection.find_one({'name': screen_name})
    return user


async def get_tweets_from_user(screen_name):
    user = await get_user_by_screen_name(screen_name)
    for tweet in user['tweets']:
        print(tweet['text'])


loop = asyncio.get_event_loop()
task = loop.create_task(get_tweets_from_user('MicroPoesia'))
loop.run_until_complete(task)
