import os
from concurrent.futures import ThreadPoolExecutor
from typing import Union

from botocore import exceptions

from cloudlog_commons.cloud import DynamoTable
from cloudlog_commons.shared import logger

from .utils import DynamoPutRequest, SQSRequest, SQSResponse


DYNAMO_TABLE_NAME = os.environ["DYNAMO_TABLE_NAME"]
dynamo = DynamoTable(DYNAMO_TABLE_NAME)


def handler(event: dict, context: dict):
    response = SQSResponse()
    requests = tuple(SQSRequest.from_event_list(event["Records"]))

    if len(requests):
        logger.info(f"Recieved {len(requests)} parsed requests")

        with ThreadPoolExecutor(10) as exec:
            failed_ids = exec.map(message_async_handler, requests)

            for id in failed_ids:
                id and response.add_failed_record(id)

    return response.emit()


def message_async_handler(request: SQSRequest) -> Union[str, None]:
    try:
        dynamo.execute(DynamoPutRequest(request.body))
        logger.info(f"Dynamo put request executed")

    except exceptions.ClientError as exc:
        logger.exception(exc)
        return request.id
