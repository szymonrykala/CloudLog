from decimal import Decimal
from dataclasses import dataclass
from enum import Enum


class OS(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"


class LogType(str, Enum):
    SYSTEM = "system"
    APP = "application"
    LOGGER = "logger"


@dataclass
class Log:
    os: OS
    severity: int
    message: str
    timestamp: Decimal
    hostname: str
    unit: str
    raw: str
    type: LogType
