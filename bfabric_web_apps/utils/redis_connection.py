
from .config import settings as config

from redis import Redis

if config.REDIS_USERNAME and config.REDIS_PASSWORD:
    redis_conn = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        username=config.REDIS_USERNAME,
        password=config.REDIS_PASSWORD
    )
else:
    redis_conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
