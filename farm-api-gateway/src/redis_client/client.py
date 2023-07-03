import ujson
import logging
import inspect
import asyncio
import redis.asyncio as redis
from redis.client import PubSub
from typing import Callable, Dict

from src import constants
from src.abstractions import AbsRedisMixin, AbsRedisClient

class RedisPubSubMixin(AbsRedisMixin):
    logger: logging.Logger

    def get_subscriber(self) -> PubSub:
        return self.slave_client.pubsub()

    async def handle_pubsub_msg(
        self,
        subscriber: PubSub,
        handler: Callable,
        handler_kwargs: Dict = {},
        sleep_time: float = 0.1,
        ignore_subscribe_messages: bool = False
    ):
        # Message Received: {'type': 'pmessage', 'pattern': b'channel:*', 'channel': b'channel:1', 'data': b'Hello'}
        while True:
            data = await subscriber.get_message(ignore_subscribe_messages)
            if data:
                message = data['data']
                if message:
                    try:
                        await handler(ujson.loads(message), **handler_kwargs)
                        continue
                    except Exception as e:
                        self.logger.exception(f'redis {subscriber=} handle {message=} get exception {e}')
                        continue
            await asyncio.sleep(sleep_time)

    async def subscribe(
        self,
        channel: str,
        handler: Callable,
        handler_kwawrgs: Dict = {},
        sleep_time: float = 0.1
    ):
        """_summary_

        Args:
            channel (str): _description_
            handler (Callable): _description_
            handler_kwawrgs (Dict, optional): _description_. Defaults to {}.
            sleep_time (float, optional): _description_. Defaults to 0.1.

        Raises:
            ValueError: _description_
        """
        if not inspect.iscoroutinefunction(handler):
            raise ValueError('handler must be a coroutine')

        subscriber: PubSub = self.get_subscriber()
        await subscriber.subscribe(channel, ignore_subscribe_messages=True)
        task = asyncio.create_task(
            self.handle_pubsub_msg(subscriber, handler, handler_kwawrgs, sleep_time, True)
        )
        self.logger.info(f'RedisPubSubMixin subscribe {channel=} with {handler} -> {task=}')

    async def publish(self, channel: str, message: Dict):
        """_summary_

        Args:
            channel (str): _description_
            message (str): _description_

        Raises:
            ValueError: _description_
        """
        if not channel or not isinstance(channel, str):
            raise ValueError('channel must be an instance of string')

        if isinstance(message, dict):
            dumpped_msg = ujson.dumps(message)
        else:
            raise ValueError('accept message is an instance of dict or core.abstractions.CustomBaseModel')

        return await self.client.publish(channel, dumpped_msg)


class RedisClient(RedisPubSubMixin, AbsRedisClient):
    def __init__(self, **kwargs) -> None:
        self._client: redis.Redis = None
        self._name: str = None
        self._is_connected: bool = False
        self.logger = kwargs.get('logger') or logging.getLogger(constants.CONSOLE_LOGGER)

    @property
    def is_connected(self):
        return self._is_connected

    @property
    def client(self) -> redis.Redis:
        return self._client

    @property
    def slave_client(self) -> redis.Redis:
        return self._client

    async def connect(
        self,
        server_url: str,
        decode_responses: bool = True,     # response is bytes (default)
        **kwargs
    ):
        if isinstance(self._client, redis.Redis):
            return
        try:
            self._client = redis.Redis.from_url(
                server_url,
                decode_responses=decode_responses
            )
            self._name = f'Redis-Client-{server_url}'
            self._is_connected = True
            self.logger.info(f'RedisClient {self._name} | connected {self._is_connected}')
        except Exception as e:
            self.logger.exception(f'connect redis {server_url=} get exception {e}')

        return self._client

    async def disconnect(self, *args, **kwargs):
        if self._client and isinstance(redis.Redis):
            await self._client.close()