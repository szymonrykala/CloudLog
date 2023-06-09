import os
import signal

from worker import LogWorker

from cloudlog_commons.services import LogQueue, LogSender
from cloudlog_commons.shared.logger import setupFileLogger, setupStdoutLogger

__queue: LogQueue
__sender: LogSender


def cloudlog_daemon_factory():
    global __queue, __sender
    logger = setupStdoutLogger()
    # logger = setupFileLogger()

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
        
    signal.signal(
        signal.SIGINT, 
        stop_handler
    ) #handling systemd signal
        