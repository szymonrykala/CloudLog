from datetime import datetime
from logging import getLogger, DEBUG, INFO, FileHandler, StreamHandler, Formatter
import os
import sys

LOGGER_NAME = "ClouLogSystem"
DEBUG_MODE_ON = os.environ.get("DEBUG_MODE", "false").lower() == "true"


logger = getLogger(LOGGER_NAME)


def __set_lvl(_logger=logger):
    _logger.setLevel(DEBUG if DEBUG_MODE_ON else INFO)


def __set_format(_handler):
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    _handler.setFormatter(formatter)


def setupStdoutLogger(logger_instance=logger):
    h = StreamHandler(sys.stdout)
    __set_format(h)

    logger_instance.addHandler(h)
    __set_lvl(logger_instance)
    return logger_instance


def setupFileLogger(logger_instance=logger):
    logfile_name = f"./logs/{datetime.now().isoformat().replace(':','-')}.txt"
    file_handler = FileHandler(logfile_name, mode="w+")

    logger_instance.addHandler(file_handler)
    __set_lvl(logger_instance)
    return logger_instance


__set_lvl()
