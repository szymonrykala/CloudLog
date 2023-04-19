import os
from queue import Queue
import queue
import threading
import requests
import time

from . import Log

# TODO: If we want to use logger there instead of prints, we have to ensure that its not using our handler, otherwise we will get recursion loop
class LogSender(threading.Thread):
    stopped: bool = False
    log_queue: Queue = Queue()

    endpoint: str
    batch_size: int
    send_interval: int

    def __init__(self, endpoint=None, batch_size=None, send_interval=None):
        super().__init__()
        self.endpoint = endpoint if endpoint else os.environ["CLOUDLOG_ENDPOINT"]
        self.batch_size = batch_size if batch_size else os.environ.get("CLOUDLOG_BATCH_SIZE", 25)
        self.send_interval = send_interval if send_interval else os.environ.get("CLOUDLOG_SEND_INTERVAL", 10)

    def stop(self):
        self.stopped = True

    def write_log(self, log: Log) -> bool:
        if log is None or type(log) != Log:
            return False

        self.log_queue.put(log)
        return True

    def write_logs(self, logs: list[Log]) -> bool:
        if logs is None or type(logs) != list:
            return False

        for log in logs:
            self.write_log(log)

        return True

    def run(self):
        while not self.stopped:
            batch = []
            while len(batch) < self.batch_size:
                try:
                    batch.append(self.log_queue.get(block=False)) # No need to block, we rerun it every now and then anyway
                except queue.Empty:
                    break

            try:
                response = requests.post(self.endpoint, json=batch)
                if response.status_code == 200:
                    print(f"Sent batch with {len(batch)} logs")
                else:
                    print(f"Failed to send logs with status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send logs: {e}")

            time.sleep(self.send_interval)