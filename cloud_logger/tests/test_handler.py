import logging
import os

import pytest

from cloudlog_commons import LogQueue


@pytest.mark.parametrize("log_count", (
    (0),
    (5),
))
def test_local_handler(monkeypatch: pytest.MonkeyPatch, log_count: int):
    envs = {
        'CLOUDLOG_ENDPOINT': ''
    }
    monkeypatch.setattr(os, 'environ', envs)

    from cloudlogger import CloudLogHandler

    logger = logging.getLogger('test_logger')
    assert len(logger.handlers) == 0

    clh = CloudLogHandler('test_app')
    logger.addHandler(clh)
    logger.setLevel(logging.INFO)

    assert isinstance(clh.queue, LogQueue)
    assert len(clh.queue.pop(amount = 50)) == 0

    for i in range(log_count):
        logger.info(f'log {i} message')

    assert len(clh.queue.pop(amount = 50)) == log_count

    logger.removeHandler(clh)