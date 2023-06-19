import json
from dataclasses import asdict, dataclass
from datetime import datetime
from random import shuffle
from typing import Any

from cloudlog_commons.cloud.log import MockedLog
from cloudlog_commons.shared import Log


@dataclass
class SQSRequestEventMock:
    messageId: str
    body: list[Log]

    @classmethod
    def filled(cls, valid_count:int, invalid_count:int)->dict[str, Any]:
        logs = list(MockedLog.with_() for _ in range(valid_count)) + list(
            MockedLog.with_(os="invalid") for _ in range(invalid_count)
        )
        shuffle(logs)
        
        return asdict(cls(
            str(datetime.utcnow().timestamp()),
            json.dumps(logs)
        ))