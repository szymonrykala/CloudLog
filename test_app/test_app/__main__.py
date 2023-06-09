import logging
import sys
from time import sleep

from cloud_logger import CloudLogHandler


logger = logging.getLogger("Marek")

handlers = (
    CloudLogHandler("test-app", endpoint="local", send_interval=10),
    logging.StreamHandler(sys.stdout),
)

for handler in handlers:
    logger.addHandler(handler)

logger.setLevel(logging.DEBUG)

logger.info("Program starting ...")

# while True:
for  i in range(5):
    logger.info("taka sobie wiadomość")

    sleep(3)
