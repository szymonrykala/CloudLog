from decimal import Decimal
import json
from dataclasses import asdict, dataclass, field

from cloudlog_commons import DynamoRequest, DBLog, logger
from cloudlog_commons.exceptions import LogEntryValidationError


@dataclass
class SQSResponse:
    batchItemFailures: list = field(init=False, default_factory=list)

    def add_failed_record(self, message_id: str) -> None:
        self.batchItemFailures.append({
            "itemIdentifier": message_id
        })

    def emit(self) -> dict:
        return asdict(self)


@dataclass
class SQSRequest:
    id: str
    body: list[DBLog]

    @classmethod
    def from_event(cls, event: dict):
        event_body = json.loads(event["body"])
        logs = []
        
        for log_entry in event_body:
            try:
                logs.append(DBLog(**log_entry))
            except LogEntryValidationError as exc:
                logger.warning(exc)
            
        return cls(event["messageId"], logs)


    @classmethod
    def from_event_list(cls, event_list:tuple[dict]):
        for event in event_list:
            request = cls.from_event(event)
            if request.body:
                yield request


class DynamoPutRequest(DynamoRequest):
    def __init__(self, records: tuple[DBLog]) -> None:
        self.records = records

    def _query(self, table: object) -> None:
        with table.batch_writer() as batch:
            logger.debug(f"Writing to database")

            for record in self.records:
                data = asdict(record)
                data.update({
                    'timestamp': Decimal(data["timestamp"])
                })
                batch.put_item(Item=data)

        logger.debug(f"Writing to database finished")
