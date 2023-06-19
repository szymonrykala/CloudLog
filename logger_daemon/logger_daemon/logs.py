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
        unit = log.get("_EXE") or log.get("_AUDIT_FIELD_PROFILE", "unknown")
        
        if re.search(r"(snap)|(opt)", unit):
            log_type = LogType.APP.value

        return cls(
            os=OS.LINUX.value,
            severity=int(log.get("PRIORITY") or log.get("SYSLOG_FACILITY", 5)),
            message=log["MESSAGE"],
            timestamp=int(log["__REALTIME_TIMESTAMP"]) / 1_000_000,
            hostname=log["_HOSTNAME"],
            unit=unit,
            raw=json.dumps(log),
            type=log_type,
        )