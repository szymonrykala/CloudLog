import os

from cloudlog_commons import DBLog, DynamoTable, logger
from cloudlog_commons.exceptions import CloudLogBaseException

from .database import ReadRequest
from .request import RequestParams
from .utils import HTTPResponse

DYNAMO_TABLE_NAME = os.environ["DYNAMO_TABLE_NAME"]
dynamo = DynamoTable(DYNAMO_TABLE_NAME)


def handler(event, context):
    logger.debug(event)
    try:
        params = RequestParams.from_event(event)
        logger.info(f"Recieved parsed query {params}")

        logs:tuple[DBLog] = dynamo.execute(ReadRequest(params))

        logger.info(f"Sending {len(logs)} records..")
        return HTTPResponse.success(logs)

    except CloudLogBaseException as exc:
        logger.exception(exc)
        return HTTPResponse.error(exc)
    
    except Exception as exc:
        return HTTPResponse.error(
            CloudLogBaseException()
        )
