import logging
import sys
from time import sleep

from cloud_logger import CloudLogHandler


logger = logging.getLogger("Marek")

handlers = (
    CloudLogHandler("test-app", send_interval=15),
    logging.StreamHandler(sys.stdout),
)

for handler in handlers:
    logger.addHandler(handler)

logger.setLevel(logging.DEBUG)

logger.info("TEST-APP - Program starting ...")

# while True:
for  i in range(8):
    logger.info(f"TEST-APP - taka sobie wiadomość nr {i}")

    sleep(3)
