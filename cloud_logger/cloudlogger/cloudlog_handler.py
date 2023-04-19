from logging import Handler, LogRecord
import os
import platform

from cloudlog_commons import LogSender, Log, LogType

class CloudLogHandler(Handler):
    sender: LogSender
    app_name: str

    def __init__(self, app_name: str, logging_endpoint=None):
        Handler.__init__(self=self)

        self.app_name = app_name
        self.sender = LogSender(logging_endpoint)

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

        self.sender.write_log(log)