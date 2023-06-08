import os
from logging import DEBUG, INFO, getLogger, StreamHandler
import signal
import sys
from cloudlog_commons.log_queue import LogQueue
from cloudlog_commons.log_sender import LogSender
from worker import LogWorker

__queue: LogQueue
__sender: LogSender


def __setup_logger():
    debug_mode = bool(os.environ.get("CLOUDLOG_DEBUG_MODE"))

    logger = getLogger("CloudLog")
    logger.addHandler(StreamHandler(sys.stdout))
    logger.setLevel(DEBUG if debug_mode else INFO)
    return logger


def cloudlog_daemon_factory():
    global __queue, __sender
    logger = __setup_logger()

    __queue = LogQueue()
    LogSender.attach_queue(__queue)
    LogWorker.attach_queue(__queue)

    interval = int(os.environ.get("DAEMON_INTERVAL", 15))

    __sender = LogSender(
        os.environ.get("CLOUDLOG_BATCH_SIZE", 50),
        os.environ.get("CLOUDLOG_SEND_INTERVAL", interval + 1),
        os.environ["CLOUDLOG_ENDPOINT"],
    )

    return LogWorker(interval, logger)


if __name__ == "__main__":
    daemon = cloudlog_daemon_factory()
    daemon.start()

    def stop_handler(*_):
        global __sender, __queue
        __sender.stop()
        daemon.stop()
        del __queue, __sender
        
    signal.signal(
        signal.SIGINT, 
        stop_handler
    ) #handling systemd signal
        