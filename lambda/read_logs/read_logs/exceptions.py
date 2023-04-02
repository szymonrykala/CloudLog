
from dataclasses import asdict, dataclass


@dataclass
class LogsReaderException(Exception):
    statusCode: int = 500
    message: str = "InternalServerError"

