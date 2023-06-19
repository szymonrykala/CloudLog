import json
from dataclasses import asdict

import pytest

from cloudlog_commons.cloud import DBLog
from cloudlog_commons.cloud.exceptions import LogEntryValidationError
from cloudlog_commons.cloud.log import MockedLog
from cloudlog_commons.shared import OS, LogType


@pytest.mark.parametrize("data, success", (
    ({}, False),
    (MockedLog.with_(), True),
    (MockedLog.with_(timestamp=123, hostname="zupa"), False),
    (MockedLog.with_(os="RedHat"), False),
    (MockedLog.with_(type="unsupported"), False),
))
def test_log(data:dict, success:bool):
    if success:
        log = DBLog(**data)

        assert isinstance(log, DBLog)
        assert isinstance(log.id, str)
        assert isinstance(log.os, OS)
        assert isinstance(log.type, LogType)
        assert isinstance(log.severity, int)
        assert isinstance(log.timestamp, float)

        for field in ('message', 'hostname', 'unit', 'raw'):
            assert isinstance(log.__getattribute__(field), str)

        assert json.dumps(asdict(log))

    else:
        with pytest.raises(LogEntryValidationError):
            DBLog(**data)