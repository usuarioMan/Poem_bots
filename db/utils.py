from bson.json_util import dumps
from aiofiles import open as aiopen
from db.motor_client import MotorClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCursor

from exceptions.database_operations import FatalError


def get_motor_client() -> MotorClient:
    try:
        motor_client = MotorClient()
        return motor_client

    except Exception as error:
        raise FatalError(error)


async def check_if_database_exists(database_name):
    motor_client = get_motor_client()
    dbs_on_server = await motor_client.motor.list_database_names()
    try:
        if database_name not in dbs_on_server:
            raise Exception

    except Exception as error:
        print(error)


def motor_global_init():
    try:
        MotorClient()
    except Exception as error:
        raise FatalError(error)


def get_motor() -> AsyncIOMotorClient:
    try:
        motor_client = MotorClient()
        return motor_client.motor
    except Exception as error:
        raise FatalError(error)


async def collection_to_file(cursor: AsyncIOMotorCursor, file: str):
    try:
        async with aiopen(file, mode='w+') as f_out:
            async for document in cursor:
                await f_out.write(dumps(document))

            return f_out
    except Exception as error:
        raise FatalError(error)


async def get_user(username: str) -> dict:
    try:
        client = get_motor_client()
        collection = client.get_collection('poeta', 'users')
        return await collection.find_one({"username": username}, {'_id': 0})
    except Exception as error:
        raise FatalError(error)
