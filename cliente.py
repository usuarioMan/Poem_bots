from aiohttp import ClientSession


# noinspection PyProtectedMember
class Cliente:
    __client = None

    def __new__(cls) -> "ClientSession":
        if cls.__client is None:
            cls.__client = object.__new__(cls)
            cls.__client.async_client = ClientSession()

        return cls.__client.async_client


def get_session() -> ClientSession:
    return Cliente()


def get_http_client() -> ClientSession:
    return Cliente()
