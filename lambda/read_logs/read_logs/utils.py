import json
from dataclasses import asdict, dataclass

from cloudlog_commons import DBLog
from cloudlog_commons.exceptions import CloudLogBaseException


@dataclass
class HTTPResponse:
    statusCode: int
    body: str

    def __init__(self, code:int, body:dict) -> None:
        self.statusCode = code
        self.body = json.dumps(body)

    @classmethod
    def success(cls, records: tuple[DBLog]):
        body = tuple(asdict(record) for record in records)

        return asdict(cls(200, body))

    @classmethod
    def error(cls, exc: CloudLogBaseException):
        return asdict(cls(exc.statusCode, {"message": exc.message}))
