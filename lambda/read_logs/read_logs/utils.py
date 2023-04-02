


from dataclasses import asdict, dataclass
import json
from cloudlog_commons.types import Log


@dataclass
class LogRecord(Log):
    id: str
    

@dataclass
class HTTPResponse:
    statusCode: int
    body: str
    
    @classmethod
    def success(cls, records: tuple[LogRecord]):
        body = tuple(asdict(record) for record in records)
                
        return cls(
            200,
            json.dumps(body)
        )
    
    @classmethod
    def error(cls, exc)