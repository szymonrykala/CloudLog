from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from cloudlog_commons.log import LogType

from .exceptions import BadRequestParameterValue


@dataclass
class RequestParams:
    service: Optional[str] = None
    hostname: Optional[str] = None
    logType: Optional[LogType] = None
    severity: int = field(default=0)
    fromDate: datetime = field(default=datetime.utcnow() - timedelta(hours=1))
    toDate: datetime = field(default=datetime.utcnow())

    @classmethod
    def from_event(cls, event: dict):
        parser = FieldValueParser(event["queryStringParameters"] or {})

        resolvers = {
            "fromDate": lambda f: parser.date(f),
            "toDate": lambda f: parser.date(f),
            "logType": lambda f: parser.log_type(f),
            "severity": lambda f: int(parser.params[f]),
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
            return datetime.fromisoformat(self.params.get(field))
        except Exception:
            raise BadRequestParameterValue(
                f"Date field '{field}' has to be in ISO format"
            )
            
    def log_type(self, field:str) -> LogType:
        val = self.params[field].lower()
        if val in list(LogType):
            return LogType(val)

        raise BadRequestParameterValue(
            f"Value of 'logType' has to be on of ({LogType.SYSTEM},{LogType.APP},{LogType.LOGGER})"
        )
        

    def value(self, field: str):
        return self.params[field]
