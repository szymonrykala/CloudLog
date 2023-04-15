from abc import ABC, abstractmethod
from typing import Generator, Union

import boto3


class DynamoRequest(ABC):
    def execute(self, table: object):
        return self._query(table)

    @abstractmethod
    def _query(self, table: object) -> tuple[dict]:
        pass


class DynamoTable:

    def __init__(self, table_name: str) -> None:
        self.table = boto3.resource('dynamodb').Table(table_name)

    def execute(self, query: DynamoRequest) -> Union[tuple[object], Generator[object, None, None]]:
        return query.execute(self.table)
