from decimal import Decimal

from cloudlog_commons.cloud import DBLog, DynamoRequest
from cloudlog_commons.shared import LogType, logger

from .request import RequestParams


class ReadRequest(DynamoRequest):

    def __init__(self, params: RequestParams) -> None:
        self.params = params
        
        self.__att_names = {
            '#t': 'timestamp', 
            '#severity': 'severity'
        }
        self.__att_values = {
            ':tto': Decimal(self.params.toDate.timestamp()),
            ':tfr': Decimal(self.params.fromDate.timestamp()),
            ':severity': self.params.severity
        }
        self.__exp = " AND ".join((
            "#t BETWEEN :tfr AND :tto",
            "#severity <= :severity"
        ))
        
        for f in ('unit', 'hostname', 'type'):
            value = params.__getattribute__(f)
            if value:
                self.__att_names[f"#{f}"] = f
                self.__att_values[f":{f}"] = params.__getattribute__(f)
                self.__exp += f" AND #{f}=:{f}"
        
        if params.type:
            self.__att_names[f"#{f}"] = f
            self.__att_values[f":{f}"] = params.__getattribute__(f)
            self.__exp += f" AND #{f}=:{f}"

        logger.info(f"Built DB query: {self.__exp}; values:{self.__att_values}")          


    def _query(self, table: object) -> tuple[LogType]:
        response = table.scan(
            ExpressionAttributeNames=self.__att_names,
            ExpressionAttributeValues=self.__att_values,
            FilterExpression=self.__exp
        )

        return tuple(DBLog(**item) for item in response["Items"])
