import asyncio
import pymongo
import uvicorn
from fastapi import FastAPI
# from db.utils import motor_global_init, get_motor

app = FastAPI()


def config_database():
    loop = asyncio.get_event_loop()
    motor_global_init(io_loop=loop)


def run_server():
    loop = asyncio.get_event_loop()
    server_configuration = uvicorn.Config(
        app="main:app",
        host='127.0.0.1',
        port=8080,
        loop=loop,
        reload=True
    )
    server = uvicorn.Server(server_configuration)
    loop.run_until_complete(server.serve())

def config():
    config_database()

def main():
    config()
    run_server()


if __name__ == '__main__':
    main()

else:
    config()
