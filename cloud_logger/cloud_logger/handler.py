import platform
from logging import Handler, LogRecord

from cloudlog_commons.services import LogQueue
from cloudlog_commons.shared import Log, LogType, OS


class CloudLogHandler(Handler):
    queue: LogQueue = None

    def __init__(self, app_name: str):
        super().__init__()
        self.app_name = app_name

        self.os = self.__get_os_name()
        self.hostname = platform.uname().node

    @classmethod
    def attach_queue(cls, queue: LogQueue):
        cls.queue = queue

    def __get_os_name(self):
        if platform.system() == "Windows":
            return OS.WINDOWS.value
        return OS.LINUX.value

    def emit(self, record: LogRecord):
        log: Log = Log(
            os=self.os,
            severity=record.levelno,
            message=record.getMessage(),
            timestamp=record.created,
            hostname=self.hostname,
            unit=self.app_name,
            raw=record.__dict__,
            type=LogType.LOGGER,
        )

        self.queue.push(log)
