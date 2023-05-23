from .log import DBLog, Log, OS, LogType
from .database import DynamoTable, DynamoRequest
from .logger import logger
from .log_sender import LogSender
from .log_queue import LogQueue

queue = LogQueue()
LogSender.attach_queue(queue)