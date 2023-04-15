import pytest
from .utils import SQSRequestEventMock


@pytest.mark.parametrize("event, success", (
    ({
        'Records': [SQSRequestEventMock.filled(5, 1),
                    SQSRequestEventMock.filled(5, 3)]
    }, True),
))
def test_handler(event: dict, success: bool):
    from save_logs.main import handler

    resp = handler(event, {})

    assert isinstance(resp, dict)

    if success:
        assert resp == {
            'batchItemFailures': []
        }
    else:
        pass
