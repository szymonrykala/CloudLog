from dataclasses import asdict
from datetime import datetime
from cloudlog_commons.log import LogType
import pytest

from read_logs.request import FieldValueParser, RequestParams
from read_logs.exceptions import BadRequestParameterValue
from .data import EMPTY_API_EVENT


PARSER_PAYLOAD = {
    "value": "Szymon",
    "date": "2022-12-12T10:33:00",
    "wrong_date": "2022-124-12T100"
}


@pytest.fixture
def mocked_parser():
    yield FieldValueParser(PARSER_PAYLOAD)


@pytest.mark.parametrize("field, success", (
    ("date", True),
    ("wrong_date", False)
))
def test_field_value_parser_date(field, success, mocked_parser):
    if success:
        value = mocked_parser.date(field)
        assert isinstance(value, datetime)
    else:
        with pytest.raises(BadRequestParameterValue):
            mocked_parser.date(field)


@pytest.mark.parametrize("event_params, success", (
    ({}, True),
    (None, True),
    ({
        "unit": "test_service",
        "hostname": "my-machine",
        "unknown-key": "value",
        "type": "application"
    }, True),
    ({
        "type": "Bad value"
    }, False),
    ({
        "fromDate": "2012-14-11T10:00:11"
    }, False),
    ({
        "fromDate": "2023-05-21T12:51:50.235Z"
    }, True),
     ({
        "fromDate": datetime.utcnow().isoformat()
    }, True),
))
def test_request_params(event_params, success):
    EMPTY_API_EVENT["queryStringParameters"] = event_params
    event = EMPTY_API_EVENT

    if success:
        params = RequestParams.from_event(event)
        assert isinstance(params, RequestParams)
        assert isinstance(params.fromDate, datetime)
        assert isinstance(params.toDate, datetime)
        
        assert params.fromDate.timestamp() < params.toDate.timestamp()

        params_dict = params.asdict()
        assert isinstance(params_dict, dict)

        if not event_params:
            assert params_dict["severity"] == 0
            assert params_dict["fromDate"] < datetime.utcnow()
            assert params_dict["toDate"] > datetime.utcnow()

            for field in ('unit', 'hostname', 'type'):
                assert field not in params_dict
                assert field in asdict(params)

        else:
            if "type" in event_params:
                assert isinstance(params.type, LogType)

            for field in event_params.keys():
                if field in RequestParams.__dataclass_fields__:
                    assert field in params_dict
                    assert field in asdict(params)

    else:  # NOT success
        with pytest.raises(BadRequestParameterValue):
            RequestParams.from_event(event)
