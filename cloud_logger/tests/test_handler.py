import logging
import os

import pytest

from cloudlog_commons.services import LogQueue


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

    from cloud_logger.handler import CloudLogHandler

    # Filter out diffrent handlers and assert that there are not yet CloudLogHandlers
    assert len([handler for handler in logger.handlers if isinstance(handler, CloudLogHandler)]) == 0
    
    # Check if queue exists & is empty
    assert CloudLogHandler.queue is None

    HANDLER = CloudLogHandler('test_app')
    QUEUE = LogQueue()
    CloudLogHandler.attach_queue(QUEUE)
    
    assert isinstance(CloudLogHandler.queue, LogQueue)
    assert CloudLogHandler.queue == QUEUE

    logger.addHandler(HANDLER)
    logger.setLevel(logging.INFO)

    # Filter out diffrent handlers and assert that our handler is added
    assert len([handler for handler in logger.handlers if isinstance(handler, CloudLogHandler)]) == 1
    
    assert len(QUEUE.pop(amount = 50)) == 0

    for i in range(log_count):
        logger.info(f'log {i} message')

    assert len(QUEUE.pop(amount = 50)) == log_count

    logger.removeHandler(HANDLER)
    CloudLogHandler.queue = None