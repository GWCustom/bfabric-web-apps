from rq import Queue
from .redis_connection import redis_conn as conn


def q(queue_name):
    return Queue(name=queue_name, connection=conn, default_timeout=10000000)
