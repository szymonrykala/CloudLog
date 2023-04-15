from dataclasses import asdict, dataclass
from datetime import datetime
import json
from random import shuffle
from typing import Any

from cloudlog_commons.log import Log, MockedLog


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