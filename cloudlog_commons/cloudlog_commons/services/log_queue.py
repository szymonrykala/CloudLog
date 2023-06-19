from queue import Queue, Empty as QueueEmptyExpcetion

from cloudlog_commons.shared import Log, logger


class LogQueue(Queue):
    def __init__(self, maxsize: int = 0, logger=logger):
        super().__init__(maxsize)
        self.__logger = logger

    def push(self, *logs: Log) -> None:
        self.__logger.debug(
            f"{self.__class__.__name__} - recieved logs batch size={len(logs)}"
        )
        for log in logs:
            self.put(log)

    def pop(self, amount: int = 50) -> list[Log]:
        batch = []

        while len(batch) < amount:
            try:
                batch.append(self.get(block=False))
            except QueueEmptyExpcetion:
                break

        self.__logger.debug(
            f"{self.__class__.__name__} - Logs batch requested size={len(batch)}"
        )
        return batch
