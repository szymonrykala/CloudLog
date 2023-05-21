from abc import ABC, abstractmethod
from typing import Generator, Union

import boto3

from .exceptions import CloudLogBaseException


class DynamoRequestException(CloudLogBaseException):
    statusCode:int = 400

    def __init__(self, message):
        self.message = f"Failed to execute dynamo request: {message}"
    


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
        try:
            return query.execute(self.table)
        except Exception as exc:
            raise DynamoRequestException(exc)