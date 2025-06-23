import redis
from rq import Worker, Queue, Connection
import time
import threading

def test_job():
    print("Hello, this is a test job!")
    time.sleep(10)
    print("Test job finished!")
    return

def keepalive_ping(conn, interval=60):
    """
    Periodically ping Redis to keep the TCP connection alive on platforms like Azure.
    """
    while True:
        try:
            conn.ping()
        except Exception as e:
            print("Redis keepalive ping failed:", e)
        time.sleep(interval)

def run_worker(host, port, queue_names, username=None, password=None):
    """
    Starts an RQ worker with a background Redis keepalive thread to prevent Azure from dropping idle connections.
    """

    def build_redis(protocol=2):
        
        if username and password:

            print("Connecting to Redis with authentication.")
            print(f"Host: {host}, Port: {port}, Username: {username}")

            conn = redis.Redis(
                host=host,
                port=port,
                username=username,
                password=password,
                socket_keepalive=True,
                protocol=protocol
            )

        else:

            print("Connecting to Redis without authentication.")
            print(f"Host: {host}, Port: {port}")
            
            conn = redis.Redis(
                host=host,
                port=port,
                socket_keepalive=True,
                protocol=protocol
            )
        return conn
    
    try:
        conn = build_redis(protocol=2)
    except Exception as e: 
        print("Failed to connect to Redis with protocol 2, trying protocol 3...")
        conn = build_redis(protocol=3)

    # Start Redis keepalive thread
    threading.Thread(target=keepalive_ping, args=(conn,), daemon=True).start()

    with Connection(conn):
        worker = Worker(map(Queue, queue_names))
        worker.work(logging_level="INFO")
