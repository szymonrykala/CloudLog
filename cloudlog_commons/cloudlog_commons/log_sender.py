import os
import threading
import time

import requests
from requests_auth_aws_sigv4 import AWSSigV4

from .log_queue import LogQueue

class LogSender(threading.Thread):
    # Static stuff
    queue: LogQueue = None
    @classmethod
    def attach_queue(cls, queue: LogQueue):
        cls.queue = queue



    stopped: bool = False
    endpoint: str
    batch_size: int
    send_interval: int

    def __init__(
            self,
            endpoint=None,
            batch_size=None,
            send_interval=None
        ):
        super().__init__()
        self.endpoint = endpoint or os.environ["CLOUDLOG_ENDPOINT"]
        self.batch_size = batch_size or os.environ.get("CLOUDLOG_BATCH_SIZE", 25)
        self.send_interval = send_interval or os.environ.get("CLOUDLOG_SEND_INTERVAL", 10)

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            batch = LogSender.queue.pop(self.batch_size) if LogSender.queue else []

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