import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import uuid1

from cloudlog_commons.cloud.exceptions import LogEntryValidationError
from cloudlog_commons.shared import OS, Log, LogType


@dataclass
class DBLog(Log):
    id: str

    def __init__(self, **kwargs):
        self.__validate(kwargs)

        self.id = kwargs.get("id", str(uuid1()))
        self.os = OS(kwargs["os"])
        self.type = LogType(kwargs["type"])
        self.timestamp = float(kwargs["timestamp"])
        self.severity = int(kwargs["severity"])

        for field in ("message", "hostname", "unit", "raw"):
            self.__setattr__(field, kwargs[field])

    def __validate(self, data: dict):
        if any(
            (
                data.get("os") not in list(OS),
                data.get("type") not in list(LogType),
                data.get("severity") not in range(0, 8),  # <0-7>
                not isinstance(data.get("timestamp"), (float, Decimal)),
                not re.search(r"\d{10}\.\d{1,6}", str(data.get("timestamp"))),
            )
        ):
            raise LogEntryValidationError(f"Log entry '{data}' is not valid")


@dataclass
class MockedLog:
    os: OS
    severity: int
    message: str
    timestamp: float
    hostname: str
    unit: str
    raw: str
    type: LogType
    id: str = field(init=False, default_factory=lambda: str(uuid1()))

    @classmethod
    def with_(cls, **kwargs) -> dict[str, Any]:
        defaults = {
            "os": OS.WINDOWS,
            "severity": 2,
            "message": "message form the logs",
            "timestamp": datetime.now().timestamp(),
            "hostname": "some host name",
            "unit": "some test unit",
            "raw": "raw version of the log",
            "type": LogType.SYSTEM,
        }
        defaults.update(kwargs or {})

        return asdict(cls(**defaults))
