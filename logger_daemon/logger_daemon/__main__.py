import os
import signal
import time

from worker import LogWorker

from cloudlog_commons.services import LogQueue, LogSender
from cloudlog_commons.shared.logger import setupFileLogger, setupStdoutLogger

__queue: LogQueue
__sender: LogSender


def cloudlog_daemon_factory():
    global __queue, __sender
    logger = setupStdoutLogger()
    # logger = setupFileLogger()

    __queue = LogQueue(logger=logger)
    LogSender.attach_queue(__queue)
    LogWorker.attach_queue(__queue)

    interval = int(os.environ.get("DAEMON_INTERVAL", 15))

    __sender = LogSender(
        endpoint=os.environ["CLOUDLOG_ENDPOINT"],
        batch_size=int(os.environ.get("CLOUDLOG_BATCH_SIZE", 50)),
        send_interval=int(os.environ.get("CLOUDLOG_SEND_INTERVAL", interval + 1)),
        logger=logger
    )
    __sender.start()

    return LogWorker(interval, logger)


if __name__ == "__main__":
    daemon = cloudlog_daemon_factory()
    stopped: bool = False

    def stop_handler(*_):
        global __sender
        global stopped
        daemon.stop()
        __sender.stop()
        stopped = True

    signal.signal(
        signal.SIGINT,
        stop_handler
    ) #handling systemd signal

    daemon.start()

    # On windows daemon.join() causes signals not to work
    # We had to make a workaround to be able to stop the daemon
    while not stopped:
        time.sleep(1)