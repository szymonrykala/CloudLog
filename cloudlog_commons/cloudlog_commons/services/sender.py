from dataclasses import asdict
import json
import threading
import time

import requests
from requests_auth_aws_sigv4 import AWSSigV4

from cloudlog_commons.shared import Log, logger

from cloudlog_commons.services import LogQueue


class LogSender(threading.Thread):
    queue: LogQueue = None
    stopped: bool = False

    def __init__(self, endpoint: str, batch_size: int, send_interval: int, logger=logger):
        super().__init__()
        self.endpoint = endpoint
        self.batch_size = batch_size
        self.send_interval = send_interval
        self.__logger = logger

    @classmethod
    def attach_queue(cls, queue: LogQueue):
        if not cls.queue:
            cls.queue = queue

    def __send_batch(self):
        batch: list[Log] = self.queue.pop(self.batch_size)

        if len(batch) > 0:
            self.__logger.info(f"{self.__class__.__name__} - Sending batch size={len(batch)}")
            try:
                auth = AWSSigV4("execute-api")
                body = tuple(asdict(record) for record in batch)
                self.__logger.debug(body)

                response = requests.request(
                    "PUT",
                    self.endpoint,
                    json=body,
                    auth=auth
                )

                self.__logger.debug(f"{self.__class__.__name__} - API response: {response.text}")
                if 200 <= response.status_code < 300:
                    self.__logger.info(f"{self.__class__.__name__} - Batch has been sent")
                else:
                    self.__logger.warning(
                        f"{self.__class__.__name__} - Unexpected API response: {response.status_code}"
                    )

            except Exception as e:
                self.__logger.error(f"{self.__class__.__name__} - Failed to send batch: {e}")

    def stop(self):
        if not self.stopped:
            self.__send_batch()
            self.__logger.info(f"Shutting down {self}")
        self.stopped = True

    def run(self):
        if self.queue:
            self.__logger.info(f"{self.__class__.__name__} - Processing started")
            while (not self.stopped):
                self.__send_batch()

                if not threading.main_thread().is_alive():
                    self.stop()


                time.sleep(self.send_interval)
