
from .config import settings as config

from redis import Redis

redis_conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
