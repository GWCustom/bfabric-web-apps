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
    Provides internal interface for running workers on a specified host and port.

    Args:
        host (str): The host to run
        port (int): The port to run
        queue_names (list): A list of queue names to listen to
    """
    conn = redis.Redis(host=host, port=port) 
    with Connection(conn): 
        worker = Worker(map(Queue, queue_names)) 
        worker.work()