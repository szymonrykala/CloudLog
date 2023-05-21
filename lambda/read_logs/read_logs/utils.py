import json
from dataclasses import asdict, dataclass
import os

from cloudlog_commons import DBLog
from cloudlog_commons.exceptions import CloudLogBaseException

HTTP_ORIGIN = os.environ["HTTP_REQUEST_ORIGIN"]


@dataclass
class HTTPResponse:
    statusCode: int
    body: str
    headers: dict

    def __init__(self, code:int, body:dict) -> None:
        self.statusCode = code
        self.body = json.dumps(body)
        self.headers = {
            "Access-Control-Allow-Origin": HTTP_ORIGIN
        }
        
    @classmethod
    def success(cls, records: tuple[DBLog]):
        body = tuple(asdict(record) for record in records)

        return asdict(cls(200, body))

    @classmethod
    def error(cls, exc: CloudLogBaseException):
        return asdict(cls(exc.statusCode, {"message": exc.message}))
