import logging
import asyncio
from src.settings import settings


logger = logging.getLogger()


async def event_01_connect_redis():
    logger.info('startup-event: event_02_connect_redis running...')
    from redis_client import RedisClient, RedisManager, RedisSentinelClient
    # from src.socketio_events import SocketIoRedisSubscriber
    # from src.ws import sio


async def event_02_connect_telegram():
    pass


