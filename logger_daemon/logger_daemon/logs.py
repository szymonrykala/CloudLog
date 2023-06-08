import json
import re
from dataclasses import dataclass

from cloudlog_commons.log import OS, Log, LogType


@dataclass
class WindowsLog(Log):
    def from_dict(cls, log: dict):
        log_type_map = {
            "System": LogType.SYSTEM.value,
            "Application": LogType.APP.value,
        }

        return cls(
            os=OS.WINDOWS.value,
            severity=log["Level"],
            message=log["Message"],
            timestamp=log["TimeCreated"],
            hostname=log["MachineName"],
            unit=log["ProviderName"],
            raw=json.dumps(log),
            type=log_type_map.get(log["ContainerLog"], LogType.SYSTEM.value),
        )


@dataclass
class LinuxLog(Log):
    def from_dict(cls, log: dict):
        log_type = log_type = LogType.SYSTEM.value

        if re.search(r"(snap)|(opt)", log["unit"]):
            log_type = LogType.APP.value

        return cls(
            os=OS.LINUX.value,
            severity=log["PRIORITY"],
            message=log["MESSAGE"],
            timestamp=log["__REALTIME_TIMESTAMP"] / 1_000_000,
            hostname=log["_HOSTNAME"],
            unit=log["_EXE"],
            raw=json.dumps(log),
            type=log_type,
        )
