import pytest
from read_logs.database import ReadRequest
from cloudlog_commons.database import DynamoTable
from read_logs.request import RequestParams


@pytest.mark.parametrize("request_params",(
    RequestParams(**{
        "service": "test_service",
        "hostname": "my-machine",
        "logType": "application"
    }),
    RequestParams()
))
def test_read_request(request_params:RequestParams):
    from read_logs.main import DYNAMO_TABLE_NAME
    
    table = DynamoTable(DYNAMO_TABLE_NAME)
    table.execute(ReadRequest(request_params))
