from dataclasses import dataclass
from enum import Enum


class OS(str, Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"


class LogType(str, Enum):
    SYSTEM = "System"
    APP = "Application"
    LOGGER = "CloudLogger"


@dataclass
class Log:
    os: OS
    severity: int
    message: str
    timestamp: int
    hostname: str
    unit: str
    raw: str
    log_type: LogType
