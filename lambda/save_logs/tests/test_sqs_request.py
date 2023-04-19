from typing import Generator
import pytest
from cloudlog_commons import Log
from .utils import SQSRequestEventMock

from save_logs.utils import SQSRequest, SQSResponse


@pytest.mark.parametrize("event, success", (
    ({}, False),
    (SQSRequestEventMock.filled(5, 0), True)
))
def test_sqs_request_from_event(event: dict, success: bool):
    if success:
        request = SQSRequest.from_event(event)

        assert isinstance(request, SQSRequest)
        assert len(request.body) == 5

        for row in request.body:
            assert isinstance(row, Log)

    else:
        with pytest.raises(KeyError):
            SQSRequest.from_event(event)


@pytest.mark.parametrize("event_list, success", (
    ([{}], False),
    ([SQSRequestEventMock.filled(5, 0), SQSRequestEventMock.filled(5, 0)], True)
))
def test_sqs_request_from_event_list(event_list: dict, success: bool):
    requests = SQSRequest.from_event_list(event_list)
    assert isinstance(requests, Generator)

    if success:
        for req in requests:
            assert isinstance(req, SQSRequest)

    else:
        with pytest.raises(KeyError):
            for req in requests:
                assert isinstance(req, SQSRequest)
    
            
def test_sqs_request_from_event_list_empty_body_filtering():
    events = [SQSRequestEventMock.filled(5, 0), SQSRequestEventMock.filled(0, 0)]

    requests = SQSRequest.from_event_list(events)
    
    assert len(tuple(requests)) == 1


def test_sqs_request_body_filtering():
    valid_events_count = 4

    sqs_event = SQSRequestEventMock.filled(valid_events_count, 5)
    request = SQSRequest.from_event(sqs_event)

    assert len(request.body) == valid_events_count


def test_sqs_response():
    resp = SQSResponse()

    assert len(resp.batchItemFailures) == 0
    resp.add_failed_record('test_id')

    assert len(resp.batchItemFailures) == 1
    resp_dict = resp.emit()

    assert isinstance(resp_dict, dict)
    assert resp_dict == {
        'batchItemFailures': [
            {'itemIdentifier': 'test_id'}
        ]
    }
