import logging
import os

import pytest

from cloudlog_commons import LogQueue

@pytest.mark.parametrize("log_count, logger", (
    (0, logging.getLogger('test_logger')),
    (5, logging.getLogger('test_logger')),
    (0, logging.getLogger()), # Global logger
    (5, logging.getLogger()), # Global logger
))
def test_handler(monkeypatch: pytest.MonkeyPatch, log_count: int, logger: logging.Logger):
    envs = {
        'CLOUDLOG_ENDPOINT': ''
    }
    monkeypatch.setattr(os, 'environ', envs)

    from cloudlogger import CloudLogHandler

    # Filter out diffrent handlers and assert that there are not yet CloudLogHandlers
    assert len([handler for handler in logger.handlers if isinstance(handler, CloudLogHandler)]) == 0

    clh = CloudLogHandler('test_app')
    logger.addHandler(clh)
    logger.setLevel(logging.INFO)

    # Filter out diffrent handlers and assert that our handler is added
    assert len([handler for handler in logger.handlers if isinstance(handler, CloudLogHandler)]) == 1

    # Check if queue exists & is empty
    assert isinstance(clh.queue, LogQueue)
    assert len(clh.queue.pop(amount = 50)) == 0

    for i in range(log_count):
        logger.info(f'log {i} message')

    assert len(clh.queue.pop(amount = 50)) == log_count

    logger.removeHandler(clh)