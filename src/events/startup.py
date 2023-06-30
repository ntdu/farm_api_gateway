import logging
import asyncio
from src.settings import settings
from src import constants

logger = logging.getLogger()


async def event_01_connect_redis():
    logger.info('startup-event: event_01_connect_redis running...')
    from src.redis_client import RedisClient, RedisManager


    redis_client = RedisClient()
    connect_params = (settings.get_redis_server_url(),)
    await redis_client.connect(*connect_params)

    redis_manager = RedisManager()
    redis_manager.add_pubsub_client(
        constants.REDIS_CLIENT_NAME_SUBSCRIBER,
        redis_client
    )

    logger.info('startup-event: event_01_connect_redis done')


async def event_02_connect_telegram():
    pass


events = [v for k, v in locals().items() if k.startswith("event_")]