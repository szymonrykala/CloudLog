import os

from cloudlog_commons.log_queue import LogQueue
from cloudlog_commons.log_sender import LogSender

from .handler import CloudLogHandler as LogHandler

__logs_buffer = LogQueue()
__logs_sender: LogSender = None


def CloudLogHandler(
    logger_name: str,
    endpoint: str = None,
    batch_size: int = None,
    send_interval: int = None,
) -> LogHandler:
    endpoint = endpoint or os.environ["CLOUDLOG_ENDPOINT"]
    batch_size = batch_size or os.environ.get("CLOUDLOG_BATCH_SIZE", 50)
    send_interval = send_interval or os.environ.get("CLOUDLOG_SEND_INTERVAL", 10)

    LogHandler.attach_queue(__logs_buffer)
    LogSender.attach_queue(__logs_buffer)
    __logs_sender = LogSender(endpoint, batch_size, send_interval)
    __logs_sender.start()

    return LogHandler(logger_name)
