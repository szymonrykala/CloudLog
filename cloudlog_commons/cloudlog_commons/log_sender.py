import os
import queue
import threading
import time
from queue import Queue

import requests
from requests_auth_aws_sigv4 import AWSSigV4

from . import Log

# TODO: If we want to use logger there instead of prints, we have to ensure that its not using our handler, otherwise we will get recursion loop
class LogSender(threading.Thread):
    stopped: bool = False
    log_queue: Queue = Queue()

    endpoint: str
    batch_size: int
    send_interval: int

    def __init__(
            self,
            endpoint=os.environ["CLOUDLOG_ENDPOINT"],
            batch_size=os.environ.get("CLOUDLOG_BATCH_SIZE", 25),
            send_interval=os.environ.get("CLOUDLOG_SEND_INTERVAL", 10)
        ):
        super().__init__()
        self.endpoint = endpoint
        self.batch_size = batch_size
        self.send_interval = send_interval

    def stop(self):
        self.stopped = True

    def write_log(self, log: Log) -> bool:
        self.log_queue.put(log)

    def write_logs(self, logs: list[Log]) -> bool:
        for log in logs:
            self.write_log(log)

    def run(self):
        while not self.stopped:
            batch = []
            while len(batch) < self.batch_size:
                try:
                    batch.append(self.log_queue.get(block=False)) # No need to block, we rerun it every now and then anyway
                except queue.Empty:
                    break

            if len(batch) > 0:
                try:
                    # Uses same env variables as AWS CLI
                    auth = AWSSigV4('execute-api')
                    response = requests.post(self.endpoint, json=batch, auth=auth)
                    if response.status_code == 200:
                        print(f"Sent batch with {len(batch)} logs")
                    else:
                        print(f"Failed to send logs with status code {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to send logs: {e}")

            time.sleep(self.send_interval)