import platform
from logging import Handler, LogRecord

from cloudlog_commons import Log, LogQueue, LogType, queue


class CloudLogHandler(Handler):
    queue: LogQueue
    app_name: str

    def __init__(self, app_name: str):
        super().__init__()

        self.app_name = app_name
        self.queue = queue

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