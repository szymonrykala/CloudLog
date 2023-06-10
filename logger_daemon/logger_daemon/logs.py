import json
import re
from dataclasses import dataclass

from cloudlog_commons.shared import OS, Log, LogType


@dataclass
class WindowsLog(Log):

    @classmethod
    def from_dict(cls, log: dict):
        log_type_map = {
            "System": LogType.SYSTEM.value,
            "Application": LogType.APP.value,
        }

        return cls(
            os=OS.WINDOWS.value,
            severity=int(log["Level"]),
            message=log["Message"],
            timestamp=int(log["TimeCreated"][6:-2])/1000, # Date comes in as "/Date(xxx)/"
            hostname=log["MachineName"],
            unit=log["ProviderName"],
            raw=json.dumps(log),
            type=log_type_map.get(log["ContainerLog"], LogType.SYSTEM.value),
        )


@dataclass
class LinuxLog(Log):

    @classmethod
    def from_dict(cls, log: dict):
        log_type = log_type = LogType.SYSTEM.value

        if re.search(r"(snap)|(opt)", log["_EXE"]):
            log_type = LogType.APP.value

        return cls(
            os=OS.LINUX.value,
            severity=int(log["PRIORITY"]),
            message=log["MESSAGE"],
            timestamp=int(log["__REALTIME_TIMESTAMP"]) / 1_000_000,
            hostname=log["_HOSTNAME"],
            unit=log["_EXE"],
            raw=json.dumps(log),
            type=log_type,
        )