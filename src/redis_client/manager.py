from typing import Dict

from src import constants
from src.abstractions import SingletonClass, AbsRedisClient, AbsRedisManager


class RedisManager(SingletonClass, AbsRedisManager):
    """Class Redis help to store connected client in dict
    redis_manager = RedisManager()
    single_client = RedisClient()
    await single_client.connect(...)

    sentinel = RedisSentinelClient()
    await sentinel.connect()

    redis_manager.add_cache_client(name, single_client)
    redis_manager.add_pubsub_client(name, sentinel)

    Args:
        SingletonClass (_type_): _description_
    """

    def _singleton_init(self, **kwargs):
        self._cache_clients: Dict[str, AbsRedisClient] = {}
        self._pubsub_clients: Dict[str, AbsRedisClient] = {}

    def add_cache_client(self, name: str, client: AbsRedisClient):
        if not isinstance(client, AbsRedisClient):
            raise ValueError(f'expected client is an instance of AbsRedisClient get {type(client)=}')
        self._cache_clients.update({name: client})

    def get_cache_client(self, name: str | int = constants.DEFAULT_CACHE_CLIENT_NAME) -> AbsRedisClient:
        return self._cache_clients.get(name)

    def remove_cache_client(self, name: str):
        if name in self._cache_clients:
            del self._cache_clients[name]
    
    def add_pubsub_client(self, name: str, client: AbsRedisClient):
        if not isinstance(client, AbsRedisClient):
            raise ValueError(f'expected client is an instance of AbsRedisClient get {type(client)=}')
        self._pubsub_clients.update({name: client})

    def get_pubsub_client(self, name: str | int = constants.DEFAULT_PUBUB_CLIENT_NAME) -> AbsRedisClient:
        return self._pubsub_clients.get(name)

    def remove_pubsub_client(self, name: str):
        if name in self._pubsub_clients:
            del self._pubsub_clients[name]

    async def publish_all_clients(self, *args, **kwargs):
        for name, client in self._pubsub_clients.items():
            await client.publish(*args, **kwargs)

    async def subscribe_all_clients(self, *args, **kwargs):
        for name, client in self._pubsub_clients.items():
            await client.subscribe(*args, **kwargs)
