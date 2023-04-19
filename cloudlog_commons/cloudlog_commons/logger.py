import logging
import os

LOGGER_NAME = "ClouLog"
DEBUG_MODE_ON = os.environ.get("DEBUG_MODE", 'false').lower() == 'true'


logger  = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG if DEBUG_MODE_ON else logging.INFO)
