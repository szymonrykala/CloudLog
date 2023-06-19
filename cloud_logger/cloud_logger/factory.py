import os
import signal

from cloudlog_commons.services import LogQueue, LogSender
from cloudlog_commons.shared.logger import setupFileLogger, setupStdoutLogger

from .handler import CloudLogHandler as LogHandler

__logs_buffer: LogQueue 
__logs_sender: LogSender


def CloudLogHandler(
    logger_name: str,
    endpoint: str = None,
    batch_size: int = None,
    send_interval: int = None,
) -> LogHandler:
    global __logs_buffer, __logs_sender

    endpoint = endpoint or os.environ["CLOUDLOG_ENDPOINT"]
    batch_size = int(batch_size or os.environ.get("CLOUDLOG_BATCH_SIZE", 50))
    send_interval = int(send_interval or os.environ.get("CLOUDLOG_SEND_INTERVAL", 10))

    logger = setupStdoutLogger()
    # logger = setupFileLogger()

    __logs_buffer = LogQueue(logger=logger)

    LogHandler.attach_queue(__logs_buffer)
    LogSender.attach_queue(__logs_buffer)
    __logs_sender = LogSender(
        endpoint=endpoint, 
        batch_size=batch_size, 
        send_interval=send_interval, 
        logger=logger
    )
    __logs_sender.start()
    
    def stop_handler(*_):
        __logs_sender.stop()
        __logs_sender.join()
        exit(0)

    signal.signal(
        signal.SIGINT,
        stop_handler
    ) #handling systemd signal

    return LogHandler(logger_name)
