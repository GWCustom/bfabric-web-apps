import redis 
from rq import Worker, Queue, Connection
import time

def test_job(): 

    """
    A test job that prints a message to the console.
    """
    print("Hello, this is a test job!")
    time.sleep(10) 
    print("Test job finished!")
    return



def run_worker(host, port, queue_names):
    """
    Starts an RQ (Redis Queue) worker that listens to specified queues and processes jobs.

    This worker is configured to:
    - Keep the Redis connection alive using TCP keepalive
    - Actively poll Redis every 60 seconds to prevent idle timeouts (common in cloud environments like Azure)
    - Optionally support scheduled jobs via `with_scheduler=True`

    Args:
        host (str): The Redis server hostname or IP address.
        port (int): The Redis server port.
        queue_names (list): A list of queue names the worker should listen to.

    """
    conn = redis.Redis(
        host=host,
        port=port,
        socket_keepalive=True
    )

    with Connection(conn):
        worker = Worker(map(Queue, queue_names))
        # Set job_monitoring_interval to 60 seconds to keep connection active
        worker.work(with_scheduler=True, logging_level="INFO", job_monitoring_interval=60)