from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from cloudlog_commons.shared import LogType

from .exceptions import BadRequestParameterValue


@dataclass
class RequestParams:
    unit: Optional[str] = None
    hostname: Optional[str] = None
    type: Optional[LogType] = None
    limit: int = field(default=80)
    severity: int = field(default=0)
    toDate: datetime = field(default=datetime.utcnow() + timedelta(minutes=10))
    fromDate: datetime = field(default=toDate.default - timedelta(hours=1, minutes=10))

    @classmethod
    def from_event(cls, event: dict):
        parser = FieldValueParser(event["queryStringParameters"] or {})

        resolvers = {
            "fromDate": lambda f: parser.date(f),
            "toDate": lambda f: parser.date(f),
            "type": lambda f: parser.log_type(f),
            "severity": lambda f: int(parser.params[f]),
            "limit": lambda f: int(parser.params[f]),
        }

        values_generator = (
            (field, resolvers.get(field, lambda f: parser.value(f))(field))
            for field in cls.__dataclass_fields__ if field in parser.params
        )
        params = dict(values_generator)

        return cls(**params)

    def asdict(self) -> dict:
        return {
            k:v for k,v in asdict(self).items()
            if v is not None
        }


class FieldValueParser:

    def __init__(self, raw_params: dict) -> None:
        self.params: dict = raw_params

    def date(self, field: str) -> datetime:
        try:
            return datetime.fromisoformat(self.params.get(field).replace("Z","+00:00"))
        except Exception:
            raise BadRequestParameterValue(
                f"Date field '{field}' has to be in ISO format"
            )
            
    def log_type(self, field:str) -> LogType:
        val = self.params[field].lower()
        if val in list(LogType):
            return LogType(val)

        raise BadRequestParameterValue(
            f"Value of 'type' has to be on of ({LogType.SYSTEM},{LogType.APP},{LogType.LOGGER})"
        )
        

    def value(self, field: str):
        return self.params[field]
