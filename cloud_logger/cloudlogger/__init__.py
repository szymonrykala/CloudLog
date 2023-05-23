import cloudlog_commons
from .cloudlog_handler import CloudLogHandler

queue = cloudlog_commons.LogQueue()
cloudlog_commons.LogSender.attach_queue(queue)
sender = cloudlog_commons.LogSender()