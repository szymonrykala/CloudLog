import threading
import time

import requests
from requests_auth_aws_sigv4 import AWSSigV4

from cloudlog_commons.log import Log

from .log_queue import LogQueue


class LogSender(threading.Thread):
    queue: LogQueue = None
    stopped: bool = False

    def __init__(self, endpoint: str, batch_size: int, send_interval: int):
        super().__init__()
        self.endpoint = endpoint
        self.batch_size = batch_size
        self.send_interval = send_interval

    @classmethod
    def attach_queue(cls, queue: LogQueue):
        if not cls.queue:
            cls.queue = queue

    def stop(self):
        self.stopped = True

    def run(self):
        if self.queue:
            while not self.stopped:
                batch: tuple[Log] = self.queue.pop(self.batch_size)

                if len(batch) > 0:
                    try:
                        # Uses same env variables as AWS CLI
                        auth = AWSSigV4("execute-api")
                        response = requests.post(self.endpoint, json=batch, auth=auth)
                        if response.status_code == 200:
                            print(f"Sent batch with {len(batch)} logs")
                        else:
                            print(f"Failed to send logs: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to send logs: {e}")

                time.sleep(self.send_interval)
