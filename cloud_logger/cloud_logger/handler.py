import json
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
    
    def __map_severity(self, python_lvl:int) -> int:
        return {
            0: 7,
            10: 7,
            20: 6,
            30: 4,
            40: 3,
            50: 2
        }[python_lvl]


    def emit(self, record: LogRecord):
        log: Log = Log(
            os=self.os,
            severity=self.__map_severity(record.levelno),
            message=record.getMessage(),
            timestamp=float(record.created),
            hostname=self.hostname,
            unit=self.app_name,
            raw=json.dumps(record.__dict__),
            type=LogType.LOGGER.value,
        )

        self.queue.push(log)
