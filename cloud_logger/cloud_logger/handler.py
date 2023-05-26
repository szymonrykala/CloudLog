import platform
from logging import Handler, LogRecord

from cloudlog_commons import LogType, Log
from cloudlog_commons.log_queue import LogQueue


class CloudLogHandler(Handler):
    queue: LogQueue

    def __init__(self, app_name: str):
        super().__init__()
        self.app_name = app_name

    @classmethod
    def attach_queue(cls, queue: LogQueue):
        cls.queue = queue

    def emit(self, record: LogRecord):
        uname: platform.uname_result = platform.uname()
        log: Log = Log(
            uname.system,
            record.levelno,
            record.getMessage(),
            record.created,
            uname.node,
            self.app_name,
            record.__dict__,
            LogType.LOGGER,
        )

        self.queue.push(log)
